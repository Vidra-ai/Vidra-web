"""Tests de enumeración SSH pasiva contra vidra-central.

Estos tests realizan comprobaciones pasivas y no destructivas contra el
servidor SSH del host de producción. No intentan autenticación con
credenciales reales ni realizan ningún tipo de fuerza bruta.

Requisito: instalar paramiko (pip install paramiko).

Por defecto estos tests están desactivados. Para ejecutarlos:
    TEST_SSH=1 pytest backend/tests/test_ssh.py -v -s

El flag -s es necesario para ver el fingerprint del host key en la salida.
"""

import os
import socket

import pytest

SSH_HOST = "178.104.197.240"
SSH_PORT = 55022
CONNECT_TIMEOUT = 10

pytestmark = pytest.mark.skipif(
    os.getenv("TEST_SSH", "0") != "1",
    reason="SSH tests disabled by default; set TEST_SSH=1 to enable",
)


class TestSSHEnumeration:
    """Enumeración pasiva del servicio SSH: puerto, banner, algoritmos y protocolo."""

    def test_ssh_port_is_open(self) -> None:
        """El puerto SSH no estándar (55022) debe estar escuchando."""
        result = socket.connect_ex((SSH_HOST, SSH_PORT))
        assert result == 0, (
            f"No se pudo conectar a {SSH_HOST}:{SSH_PORT} "
            f"(connect_ex devolvió {result}). "
            f"Verificar que el servidor está en línea y el puerto es correcto."
        )

    def test_ssh_banner_contains_openssh(self) -> None:
        """El banner SSH debe comenzar con 'SSH-2.0-OpenSSH'."""
        with socket.create_connection((SSH_HOST, SSH_PORT), timeout=CONNECT_TIMEOUT) as sock:
            banner = sock.recv(256)

        assert banner.startswith(b"SSH-2.0-OpenSSH"), (
            f"Banner inesperado: {banner[:64]!r}. "
            f"Se esperaba que comenzara con b'SSH-2.0-OpenSSH'."
        )

    def test_ssh_does_not_allow_password_auth_for_root(self) -> None:
        """El servidor no debe aceptar autenticación por contraseña para root.

        NOTA: Solo se comprueba que root+password_incorrecta falla con
        AuthenticationException. No se prueban credenciales reales.
        """
        import paramiko

        transport = paramiko.Transport((SSH_HOST, SSH_PORT))
        try:
            transport.connect()
            with pytest.raises(paramiko.AuthenticationException):
                transport.auth_password("root", "invalid_password_for_testing_only")
        finally:
            transport.close()

    def test_ssh_does_not_advertise_deprecated_algorithms(self) -> None:
        """Los algoritmos criptográficos deprecados no deben estar disponibles."""
        import paramiko

        transport = paramiko.Transport((SSH_HOST, SSH_PORT))
        try:
            transport.start_client(timeout=CONNECT_TIMEOUT)
            security_options = transport.get_security_options()

            kex_algorithms = list(security_options.kex)
            ciphers = list(security_options.ciphers)
            digests = list(security_options.digests)

            assert "diffie-hellman-group1-sha1" not in kex_algorithms, (
                "El servidor anuncia 'diffie-hellman-group1-sha1' (Logjam vulnerable). "
                f"Algoritmos kex disponibles: {kex_algorithms}"
            )

            assert "arcfour" not in ciphers, (
                "El servidor anuncia el cifrado 'arcfour' (RC4, obsoleto e inseguro). "
                f"Cifrados disponibles: {ciphers}"
            )

            assert "hmac-md5" not in digests, (
                "El servidor anuncia 'hmac-md5' (MAC débil, deprecado). "
                f"MACs disponibles: {digests}"
            )
        finally:
            transport.close()

    def test_ssh_only_uses_ssh_protocol_v2(self) -> None:
        """El banner debe anunciar SSH protocolo 2.0, nunca SSH-1.x."""
        with socket.create_connection((SSH_HOST, SSH_PORT), timeout=CONNECT_TIMEOUT) as sock:
            banner = sock.recv(256).decode("ascii", errors="replace")

        assert banner.startswith("SSH-2.0"), (
            f"El servidor no anuncia SSH protocolo 2.0. Banner: {banner[:64]!r}. "
            f"SSH-1.x tiene vulnerabilidades conocidas y no debe usarse."
        )

    def test_ssh_host_key_fingerprint_is_documented(self) -> None:
        """Obtiene e imprime el fingerprint del host key para documentación.

        # Run with -s flag to see the fingerprint for documentation purposes.
        No se hace assertion sobre el valor concreto del fingerprint (sería
        frágil ante rotaciones de clave), solo se verifica que tiene un
        formato de hash válido (longitud > 20 caracteres).
        """
        import hashlib
        import base64
        import paramiko

        host_keys = {}

        class _FingerprintPolicy(paramiko.MissingHostKeyPolicy):
            def missing_host_key(self, client, hostname, key):
                host_keys["key"] = key

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(_FingerprintPolicy())

        try:
            ssh.connect(
                SSH_HOST,
                port=SSH_PORT,
                username="nonexistent_user_for_fingerprint_only",
                password="no_password",
                timeout=CONNECT_TIMEOUT,
                allow_agent=False,
                look_for_keys=False,
            )
        except (paramiko.AuthenticationException, paramiko.SSHException):
            # Se esperan errores de autenticación; lo que importa es el host key
            pass
        finally:
            ssh.close()

        assert "key" in host_keys, (
            "No se pudo obtener el host key del servidor. "
            "Verificar conectividad y que el servidor SSH está en línea."
        )

        key = host_keys["key"]
        key_bytes = key.asbytes()
        digest = hashlib.sha256(key_bytes).digest()
        fingerprint = "SHA256:" + base64.b64encode(digest).decode().rstrip("=")

        # Imprimir para documentación (visible con pytest -s)
        print(f"\nSSH Host Key Fingerprint ({SSH_HOST}:{SSH_PORT}): {fingerprint}")
        print(f"Key type: {key.get_name()}")

        assert len(fingerprint) > 20, (
            f"El fingerprint tiene un formato inesperadamente corto: '{fingerprint}'"
        )
