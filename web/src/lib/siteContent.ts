export type Locale = "es" | "en";

export const localeLinks = {
  es: {
    switchLabel: "EN",
    switchHref: "/en",
    nav: [
      { label: "Servicios", href: "/services" },
      { label: "Proyectos", href: "/proyectos" },
      { label: "Quiénes somos", href: "/#who-we-are" },
      { label: "Blog", href: "/blog" },
      { label: "Contacto", href: "/#contact" },
    ],
    footer: [
      { label: "Servicios", href: "/services" },
      { label: "Proyectos", href: "/proyectos" },
      { label: "Quiénes somos", href: "/#who-we-are" },
      { label: "Blog", href: "/blog" },
      { label: "Contacto", href: "/contact" },
    ],
  },
  en: {
    switchLabel: "ES",
    switchHref: "/",
    nav: [
      { label: "Services", href: "/en/services" },
      { label: "Projects", href: "/en/projects" },
      { label: "Who we are", href: "/en/#who-we-are" },
      { label: "Blog", href: "/en/blog" },
      { label: "Contact", href: "/en/#contact" },
    ],
    footer: [
      { label: "Services", href: "/en/services" },
      { label: "Projects", href: "/en/projects" },
      { label: "Who we are", href: "/en/#who-we-are" },
      { label: "Blog", href: "/en/blog" },
      { label: "Contact", href: "/en/#contact" },
    ],
  },
} as const;

export const homeContent = {
  es: {
    title: "Vidra | Consultoría de IA y Estrategia de Datos para Empresas",
    description: "Expertos en soluciones de IA: Auditoría de datos, modelos predictivos y Deep Learning. Transformamos información compleja en resultados de negocio medibles.",
    hero: {
      description: "Construimos modelos ML, plataformas IA modulares y pipelines agénticos que operan en producción para empresas del sector construcción e industria.",
      ctaLabel: "Explorar servicios",
      ctaHref: "/#what-we-do",
    },
    heroSlider: {
    cta: "Explorar servicios",
    prevLabel: "Servicio anterior",
    nextLabel: "Servicio siguiente",
    slides: [
        {
            label: "Vidra Analytics",
            title: "Audita y organiza tus datos con IA",
            description: "Convertimos la información de tu negocio en bases de datos útiles, estructuradas y listas para activar.",
            imageKey: "analysis-hero",
            alt: "Consultor analizando estructuras de datos empresariales con herramientas de inteligencia artificial",
        },
        {
            label: "Motor predictivo",
            title: "Modelos predictivos de machine learning",
            description: "Desarrollamos modelos a medida para anticipar riesgos, prever demanda y apoyar mejores decisiones operativas.",
            imageKey: "machineLearning-hero",
            alt: "Científicos de datos interpretando resultados de un modelo de machine learning predictivo",
        },
        {
            label: "LLMs y Agentes",
            title: "IA generativa aplicada al negocio",
            description: "Desplegamos pipelines multi-agente y chatbots RAG que automatizan análisis, scoring e informes sobre documentación propia.",
            imageKey: "deepLearning-hero",
            alt: "Pipeline de inteligencia artificial generativa procesando documentos empresariales con modelos de lenguaje",
        },
        ],
    },
    whatWeDo: {
      eyebrow: "Qué hacemos",
      title: "Convertimos datos complejos en sistemas de IA prácticos, pensados para decidir mejor y generar valor.",
      description: "Nuestro trabajo empieza por la claridad: el problema correcto, el alcance correcto y una ruta de entrega que el equipo realmente pueda adoptar.",
      areas: [
        {
          eyebrow: "Servicio 01",
          title: "Análisis",
          description: "Evaluamos oportunidades, preparación de datos y prioridades del negocio antes de ejecutar.",
          href: "/services/analysis",
          imageKey: "analysis",
        },
        {
          eyebrow: "Servicio 02",
          title: "Machine Learning",
          description: "Construimos sistemas predictivos que mejoran la toma de decisiones con valor operativo medible.",
          href: "/services/machine-learning",
          imageKey: "machineLearning",
        },
        {
          eyebrow: "Servicio 03",
          title: "IA Generativa",
          description: "Construimos pipelines agénticos con LLMs y chatbots RAG que responden sobre la documentación propia de la empresa.",
          href: "/services/deep-learning",
          imageKey: "deepLearning",
        },
      ],
    },
    whoWeAre: {
      eyebrow: "Quiénes somos",
      title: "Un equipo multidisciplinario enfocado en la ejecución",
      body: [
        "En Vidra combinamos ciencia de datos, ingeniería de software y consultoría estratégica para entregar soluciones con valor de negocio claro y retorno medible.",
        "Priorizamos claridad técnica, disciplina operativa y detalle de implementación para que los sistemas complejos sean comprensibles, escalables y fáciles de adoptar.",
      ],
      pillars: [
        { title: "Enfoque", text: "Estrategia antes que ejecución." },
        { title: "Entrega", text: "Estructurada, medible y práctica." },
        { title: "Resultado", text: "Sistemas que las personas puedan usar." },
      ],
      ctaLabel: "Ver quiénes somos",
    },
    contact: {
      eyebrow: "Hablemos",
      title: "Hablemos de",
      highlight: "tu próxima iniciativa",
      description: "Si estás evaluando una iniciativa de IA, podemos ayudarte a definir alcance, prioridades y la ruta más práctica para avanzar.",
      contactLabel: "Ponerse en contacto",
      email: "hello@vidra.ai",
    },
  },
  en: {
    title: "Vidra | AI Consulting & Data Strategy for Enterprise",
    description: "Professional AI solutions: Data auditing, predictive modeling, and Deep Learning. We turn complex business information into measurable impact and ROI.",
    hero: {
      description: "We build ML models, modular AI platforms, and agentic pipelines that run in production for companies in construction and industry.",
      ctaLabel: "Explore services",
      ctaHref: "/en/#what-we-do",
    },
    heroSlider: {
    cta: "Explore our services",
    prevLabel: "Previous service",
    nextLabel: "Next service",
    slides: [
        {
        label: "Vidra Analytics",
        title: "Audit and organize your data with AI",
        description: "We turn raw business information into structured, useful data assets ready to activate.",
        imageKey: "analysis-hero",
        alt: "Data consultant analysing enterprise data structures with artificial intelligence tools",
        },
        {
        label: "Predictive engine",
        title: "Predictive machine learning models",
        description: "We build tailored models to anticipate risk, forecast demand, and support better operational decisions.",
        imageKey: "machineLearning-hero",
        alt: "Data scientists interpreting real-time predictive machine learning model results",
        },
        {
        label: "LLMs & Agents",
        title: "Generative AI applied to business",
        description: "We deploy multi-agent pipelines and RAG chatbots that automate analysis, scoring, and reporting over a company's own documentation.",
        imageKey: "deepLearning-hero",
        alt: "Generative AI pipeline processing enterprise documents with large language models",
        },
      ],
    },
    whatWeDo: {
      eyebrow: "What we do",
      title: "We turn complex data into practical AI systems built for decision-making and measurable value.",
      description: "Our work starts with clarity: the right problem, the right scope, and a delivery path that stakeholders can actually adopt.",
      areas: [
        {
          eyebrow: "Service 01",
          title: "Analysis",
          description: "Assess opportunities, data readiness, and business priorities before committing to execution.",
          href: "/en/services/analysis",
          imageKey: "analysis",
        },
        {
        eyebrow: "Service 02",
          title: "Machine Learning",
          description: "Build predictive systems that improve decision-making with measurable operational value.",
          href: "/en/services/machine-learning",
          imageKey: "machineLearning",
        },
        {
          eyebrow: "Service 03",
          title: "Generative AI",
          description: "We build agentic pipelines with LLMs and RAG chatbots that answer questions over a company's own knowledge base.",
          href: "/en/services/deep-learning",
          imageKey: "deepLearning",
        },
      ],
    },
    whoWeAre: {
      eyebrow: "Who we are",
      title: "A multidisciplinary team focused on execution",
      body: [
        "At Vidra, we combine data science, software engineering, and strategic consulting to deliver solutions with clear business value and measurable return on investment.",
        "Our approach prioritizes technical clarity, operational discipline, and implementation detail so complex AI systems remain understandable, scalable, and easy to adopt.",
      ],
      pillars: [
        { title: "Focus", text: "Strategy before execution." },
        { title: "Delivery", text: "Structured, measurable, and practical." },
        { title: "Outcome", text: "Systems people can actually use." },
      ],
      ctaLabel: "View who we are",
    },
    contact: {
      eyebrow: "Let’s discuss",
      title: "Let’s discuss",
      highlight: "your next initiative",
      description: "If you are evaluating an AI initiative, we can help you define scope, priorities, and the most practical path forward.",
      contactLabel: "Get in touch",
      email: "hello@vidra.ai",
    },
  },
} as const;

export const processContent = {
  es: {
    eyebrow: "Nuestro proceso",
    title: "Un modelo de entrega estructurado para reducir incertidumbre y crear valor operativo claro.",
    steps: [
      { number: "01.", title: "Análisis", outcome: "Entregable: mapa de oportunidades", description: "Evaluamos el panorama actual de datos, definimos las preguntas de negocio más relevantes e identificamos dónde habrá mayor impacto." },
      { number: "02.", title: "Prototipo", outcome: "Entregable: concepto validado", description: "Diseñamos un prototipo enfocado para validar viabilidad, alinear a los equipos y reducir el riesgo antes de escalar." },
      { number: "03.", title: "Entrenamiento", outcome: "Entregable: modelo afinado", description: "Ajustamos modelos de machine learning y deep learning mediante iteración disciplinada, medición y mejora controlada." },
      { number: "04.", title: "Integración", outcome: "Entregable: despliegue productivo", description: "Desplegamos la solución en el entorno del cliente y acompañamos su adopción con seguimiento operativo claro." },
    ],
  },
  en: {
    eyebrow: "Our process",
    title: "A structured delivery model designed to reduce uncertainty and create clear operational value.",
    steps: [
      { number: "01.", title: "Analysis", outcome: "Deliverable: opportunity map", description: "We assess the current data landscape, define the most relevant business questions, and identify where impact will be highest." },
      { number: "02.", title: "Prototype", outcome: "Deliverable: validated concept", description: "We design a focused prototype to validate feasibility, align stakeholders, and reduce delivery risk before scaling." },
      { number: "03.", title: "Training", outcome: "Deliverable: tuned model", description: "We refine machine learning and deep learning models through disciplined iteration, measurement, and controlled improvement." },
      { number: "04.", title: "Integration", outcome: "Deliverable: production rollout", description: "We deploy the solution into the client environment and support adoption with clear operational oversight." },
    ],
  },
} as const;

export const serviceContent = {
  es: {
    index: {
      eyebrow: "Servicios de consultoría",
      title: "Servicios de IA diseñados para pasar del análisis a la ejecución.",
      metaTitle: "Servicios de Consultoría en IA | Vidra",
      description: "Cada servicio está estructurado para reducir incertidumbre, definir un alcance claro y entregar un resultado práctico que el equipo pueda adoptar.",
      backLabel: "Volver al resumen",
    },
    services: [
      {
        title: "Análisis",
        metaTitle: "Análisis de Datos y Auditoría de IA | Vidra",
        metaDescription: "Evaluamos tus datos y prioridades de negocio para identificar oportunidades de IA con retorno de inversión real.",
        slug: "analysis",
        eyebrow: "Servicio 01",
        imageKey: "analysis",
        description: "Evaluamos el panorama de datos, las prioridades del negocio y las restricciones operativas para identificar dónde la IA puede generar valor medible.",
        points: ["Evaluación de oportunidades de datos", "Definición de KPI e impacto de negocio", "Priorización de casos de uso"],
      },
      {
        title: "Machine Learning",
        metaTitle: "Modelos de Machine Learning Predictivo | Vidra",
        metaDescription: "Modelos predictivos entrenados con datos históricos reales para previsión de costes, demanda y scoring automático.",
        slug: "machine-learning",
        eyebrow: "Servicio 02",
        imageKey: "machineLearning",
        description: "Entrenamos modelos ML sobre datos históricos reales del cliente y los desplegamos como APIs síncronas con intervalos de confianza.",
        points: ["Estimación de costes y previsión de demanda", "Entrenamiento con datos históricos del cliente", "Despliegue como API con validación en producción"],
      },
      {
        title: "IA Generativa y Agentes",
        metaTitle: "IA Generativa, Agentes y Chatbots RAG | Vidra",
        metaDescription: "Pipelines multi-agente con Gemini y OpenAI, y chatbots RAG sobre documentación propia para automatizar análisis e informes.",
        slug: "deep-learning",
        eyebrow: "Servicio 03",
        imageKey: "deepLearning",
        description: "Construimos pipelines multi-agente que procesan señales del mercado, documentos y datos no estructurados, y chatbots RAG sobre el conocimiento propio de la empresa.",
        points: ["Pipelines multi-agente con Gemini y OpenAI", "Chatbots RAG sobre documentación propia", "Automatización de análisis, scoring e informes"],
      },
    ],
    detail: {
      analysis: {
        title: "Análisis",
        eyebrow: "Servicio 01",
        description: "Evaluamos la estructura y madurez de los datos del cliente, identificamos los casos de uso con mayor retorno y definimos la hoja de ruta de adopción antes de ejecutar cualquier modelo.",
        heroImageKey: "analysis-hero",
        points: [
          "Diagnóstico de calidad y arquitectura de datos",
          "Identificación de casos de uso con ROI claro",
          "Definición de KPI y criterios de éxito medibles",
          "Hoja de ruta de adopción por fases",
        ],
      },
      "machine-learning": {
        title: "Machine Learning",
        eyebrow: "Servicio 02",
        description: "Entrenamos modelos predictivos sobre datos históricos reales del cliente — combinando arquitecturas LSTM, CatBoost y LightGBM — y los desplegamos como APIs síncronas con intervalos de confianza.",
        heroImageKey: "machineLearning-hero",
        points: [
          "Estimación de costes y previsión de demanda con datos reales",
          "Modelos LSTM + CatBoost + LightGBM entrenados en producción",
          "Despliegue como API con intervalos de confianza",
          "Integración con aplicaciones web y de escritorio",
        ],
      },
      "deep-learning": {
        title: "IA Generativa y Agentes",
        eyebrow: "Servicio 03",
        description: "Construimos pipelines multi-agente con Gemini que detectan, analizan y puntúan información de mercado de forma automática, y chatbots RAG con búsqueda híbrida (pgvector + pg_trgm) sobre documentación propia.",
        heroImageKey: "deepLearning-hero",
        points: [
          "Pipelines multi-agente con Gemini AI para análisis automático",
          "Chatbots RAG con búsqueda híbrida vectorial + léxica (pgvector)",
          "Scoring y clasificación de oportunidades de negocio",
          "Flujos asíncronos con entrega por API o newsletter",
        ],
      },
    },
    detailShared: {
        backLabel: "Volver a servicios",
        scopeCards: [
            {
            title: "Alcance",
            text: "Definido según prioridades de negocio y viabilidad de entrega.",
            },
            {
            title: "Resultado",
            text: "Una solución práctica que el equipo pueda adoptar y medir.",
            },
            {
            title: "Entrega",
            text: "Estructurada, colaborativa y diseñada para reducir riesgo.",
            },
        ],
        coversEyebrow: "Qué cubre este servicio",
        coversTitle: "Entrega enfocada en las partes del proyecto que más importan.",
        coversText: "Empezamos por el problema comercial, luego damos forma a la solución técnica para que siga siendo práctica, medible y alineada con el equipo.",
        ctaLabel: "Hablar sobre este servicio",
        deliveryEyebrow: "Forma de entrega",
        deliveryTitle: "Un proceso claro para equipos que necesitan confianza, no complejidad.",
        deliveryParagraphs: [
            "Definimos el problema, estructuramos el camino y validamos el alcance antes de ampliar la ejecución.",
            "El resultado es una colaboración disciplinada, directa y fácil de alinear con los equipos internos.",
        ],
        },
  },
  en: {
    index: {
      eyebrow: "Consulting services",
      title: "AI services designed to move from assessment to execution.",
      metaTitle: "AI Consulting Services | Vidra",
      description: "Each service is structured to reduce uncertainty, define a clear scope, and deliver a practical outcome that the team can adopt.",
      backLabel: "Back to overview",
    },
    services: [
      {
        title: "Analysis",
        metaTitle: "Data Analysis & AI Readiness Assessment | Vidra",
        metaDescription: "We assess your data landscape and business priorities to identify AI opportunities with clear operational value.",
        slug: "analysis",
        eyebrow: "Service 01",
        imageKey: "analysis",
        description: "We assess your data landscape, business priorities, and operational constraints to identify where AI can create measurable value.",
        points: ["Data opportunity assessment", "KPI and business impact definition", "Use case prioritization"],
      },
      {
        title: "Machine Learning",
        metaTitle: "Predictive Machine Learning Models | Vidra",
        metaDescription: "ML models trained on real historical data for cost estimation, demand forecasting, and automated scoring.",
        slug: "machine-learning",
        eyebrow: "Service 02",
        imageKey: "machineLearning",
        description: "We train ML models on the client's real historical data and deploy them as synchronous APIs with confidence intervals.",
        points: ["Cost estimation and demand forecasting", "Training on real historical client data", "API deployment with production validation"],
      },
      {
        title: "Generative AI & Agents",
        metaTitle: "Generative AI, Agents & RAG Chatbots | Vidra",
        metaDescription: "Multi-agent pipelines with Gemini and OpenAI, and RAG chatbots over a company's own documentation for automated analysis and reporting.",
        slug: "deep-learning",
        eyebrow: "Service 03",
        imageKey: "deepLearning",
        description: "We build multi-agent pipelines that process market signals, documents, and unstructured data, and RAG chatbots over a company's own knowledge base.",
        points: ["Multi-agent pipelines with Gemini and OpenAI", "RAG chatbots over company documentation", "Automated analysis, scoring, and reporting"],
      },
    ],
    detail: {
      analysis: {
        title: "Analysis",
        eyebrow: "Service 01",
        description: "We assess the structure and maturity of the client's data, identify the highest-ROI use cases, and define the adoption roadmap before building any model.",
        heroImageKey: "analysis-hero",
        points: [
          "Data quality and architecture diagnostic",
          "Use case identification with clear ROI",
          "KPI definition and measurable success criteria",
          "Phased adoption roadmap",
        ],
      },
      "machine-learning": {
        title: "Machine Learning",
        eyebrow: "Service 02",
        description: "We train predictive models on the client's real historical data — combining LSTM, CatBoost, and LightGBM architectures — and deploy them as synchronous APIs with confidence intervals.",
        heroImageKey: "machineLearning-hero",
        points: [
          "Cost estimation and demand forecasting with real data",
          "LSTM + CatBoost + LightGBM models in production",
          "API deployment with confidence intervals",
          "Integration with web and desktop applications",
        ],
      },
      "deep-learning": {
        title: "Generative AI & Agents",
        eyebrow: "Service 03",
        description: "We build multi-agent pipelines with Gemini that detect, analyse, and score market information automatically, and RAG chatbots with hybrid search (pgvector + pg_trgm) over a company's own documentation.",
        heroImageKey: "deepLearning-hero",
        points: [
          "Multi-agent pipelines with Gemini AI for automatic analysis",
          "RAG chatbots with hybrid vector + lexical search (pgvector)",
          "Scoring and classification of business opportunities",
          "Async workflows delivered via API or weekly newsletter",
        ],
      },
    },
    detailShared: {
        backLabel: "Back to services",
        scopeCards: [
            {
            title: "Scope",
            text: "Defined around business priorities and delivery feasibility.",
            },
            {
            title: "Outcome",
            text: "A practical solution the team can adopt and measure.",
            },
            {
            title: "Delivery",
            text: "Structured, collaborative, and designed to reduce risk.",
            },
        ],
        coversEyebrow: "What this service covers",
        coversTitle: "Focused delivery around the parts of the project that matter most.",
        coversText: "We start with the commercial problem, then shape the technical solution so it stays practical, measurable, and aligned with the team.",
        ctaLabel: "Discuss this service",
        deliveryEyebrow: "Delivery style",
        deliveryTitle: "A clear process built for teams that need confidence, not complexity.",
        deliveryParagraphs: [
            "We define the problem, shape the path forward, and validate the scope before expanding execution.",
            "The result is a service engagement that feels disciplined, direct, and easy to align with internal stakeholders.",
        ],
        },
  },
} as const;

export const whoWeArePageContent = {
  es: {
    title: "Sobre Vidra | Especialistas en Implementación de IA Aplicada",
    description: "Conoce a nuestro equipo multidisciplinario. Combinamos ciencia de datos e ingeniería de software para entregar soluciones de IA escalables y transparentes.",
    hero: {
      eyebrow: "Sobre nosotros",
      title: "IA aplicada para convertir datos en impacto operativo",
      body: [
        "En Vidra combinamos ciencia de datos, ingeniería de software y consultoría estratégica para crear soluciones útiles, medibles y fáciles de adoptar.",
        "Trabajamos con empresas que quieren aplicar inteligencia artificial con rigor, claridad y foco en resultados reales.",
      ],
      imageKey: "analysis",
      imageAlt: "Equipo analizando datos en un entorno de trabajo moderno",
    },
    stats: {
          focus: {
            number: "2",
            label: "Clientes activos en el sector construcción",
        },
        approach: {
            number: "3",
            label: "Proyectos en producción o en pruebas",
        },
        expertise: {
            number: "9",
            label: "Personas en el equipo",
        },
        independence: {
            number: "2",
            label: "Tipos de proyecto: ML inference y flujos agénticos",
        },
    },
    difference: {
      eyebrow: "Qué nos hace diferentes",
      title: "Claridad técnica, criterio de negocio y ejecución responsable.",
      items: [
        {
          title: "01 / Transparencia absoluta",
          text: "Explicamos el porqué y el cómo detrás de cada algoritmo. Diseñamos modelos claros donde el cliente entiende y conserva el control de la lógica de sus datos.",
        },
        {
          title: "02 / Rigor de ingeniería",
          text: "La IA solo funciona si los datos que la alimentan son sólidos. Priorizamos arquitectura, calidad y pipelines fiables antes de entrenar cualquier modelo predictivo.",
        },
        {
          title: "03 / Enfoque en ROI",
          text: "No construimos tecnología por novedad. Cada proyecto se diseña con indicadores comerciales y operativos acordados desde el primer día.",
        },
      ],
    },
    values: {
      eyebrow: "Nuestra forma de trabajar",
      title: "Principios que sostienen cada proyecto.",
      items: [
        { title: "Talento", text: "Unimos perfiles técnicos, estratégicos y creativos para resolver problemas desde varias perspectivas." },
        { title: "Dedicación", text: "Nos implicamos con disciplina en la entrega, el detalle y la adopción real de cada solución." },
        { title: "Imparcialidad", text: "Recomendamos lo que el negocio necesita, no lo que suena más llamativo en una demo." },
      ],
    },
    people: {
      eyebrow: "Nuestro equipo",
      title: "Expertos en datos, IA y estrategia aplicada.",
      text: "Combinamos perfiles técnicos y estratégicos para diseñar soluciones de IA que puedan integrarse en la operativa real del negocio.",
      cta: "Explorar carreras",
      mindsetEyebrow: "Cómo lo construimos",
        mindset: {
        strategy: {
            title: "ML Inference",
            text: "Modelos LSTM, CatBoost y LightGBM desplegados como APIs síncronas con intervalos de confianza sobre datos históricos reales del cliente.",
        },
        technology: {
            title: "Flujos agénticos",
            text: "Pipelines multi-agente asíncronos con Gemini AI para detección, análisis y scoring automático de información de mercado.",
        },
        automation: {
            title: "RAG y chatbots",
            text: "Chatbots sobre documentación propia del cliente usando pgvector, búsqueda híbrida vectorial + léxica, y OpenAI.",
        },
        partnership: {
            title: "Plataformas modulares",
            text: "Hubs extensibles React + Vite + FastAPI + Docker + Electron organizados por departamento, fáciles de crecer sin reescribir.",
        },
        },
    },
    addValue: {
        title: "Lo que construimos",
        description: "Tres tipos de sistema que ya están en producción para nuestros clientes.",
        digitaltransformation: {
          title: "Modelos ML predictivos",
          text: "Estimación de costes de obra con LSTM + CatBoost + LightGBM, entrenados sobre histórico real de partidas y desplegados como API con intervalos de confianza.",
        },
        aiImplementation: {
          title: "Pipelines agénticos",
          text: "Detección automática semanal de oportunidades de licitación privada mediante análisis multi-agente con Gemini AI, con scoring 0–100 y feedback comercial.",
        },
        dataStrategy: {
          title: "Plataformas IA modulares",
          text: "Hubs extensibles (React + Vite + FastAPI + Docker + Electron) organizados por departamento. Añadir una funcionalidad nueva es editar un registro de configuración.",
        },
    },
    journey: {
        eyebrow: "Nuestro proceso",
        title: "De la complejidad técnica a la ejecución real.",
        steps: {
            understand: {
            number: "01",
            text: "Entendemos el contexto, los objetivos y las restricciones reales del negocio.",
            },
            identify: {
            number: "02",
            text: "Identificamos oportunidades donde la IA puede aportar valor medible.",
            },
            design: {
            number: "03",
            text: "Diseñamos soluciones prácticas, escalables y alineadas con los equipos.",
            },
            implement: {
            number: "04",
            text: "Acompañamos la ejecución para que la transformación llegue al día a día.",
            },
        },
    },
    finalCta: {
        eyebrow: "Hablemos",
        title: "¿Listo para transformar la complejidad",
        highlight: "en oportunidad?",
        text: "Cuéntanos tu próximo reto y exploremos cómo convertir la ambición en progreso medible.",
        linkLabel: "Contacta con nosotros",
    },
  },
  en: {
    title: "About Vidra | Experts in Applied AI Implementation",
    description: "Meet our multidisciplinary team. We combine data science and software engineering to deliver scalable, transparent AI solutions for business.",
    hero: {
      eyebrow: "Who we are",
      title: "Applied AI to turn data into operational impact",
      body: [
        "At Vidra, we combine data science, software engineering, and strategic consulting to create useful, measurable, and easy-to-adopt solutions.",
        "We work with companies that want to apply artificial intelligence with rigor, clarity, and focus on real results.",
      ],
      imageKey: "analysis",
      imageAlt: "Team analyzing data in a modern workspace",
    }, 
    stats: {
        focus: {
            number: "2",
            label: "Active clients in the construction sector",
        },
        approach: {
            number: "3",
            label: "Projects in production or in testing",
        },
        expertise: {
            number: "9",
            label: "People in the team",
        },
        independence: {
            number: "2",
            label: "Project types: ML inference and agentic flows",
        },
    },
    difference: {
      eyebrow: "What makes us different?",
      title: "Technical clarity, business judgment, and responsible execution.",
      items: [
        {
          title: "01 / Absolute Transparency",
          text: "We explain the why and how behind every algorithm. We design white-box models where the client owns and understands the core logic of their data.",
        },
        {
          title: "02 / Engineering Rigor",
          text: "AI is only as good as the data that feeds it. We prioritize clean data architecture and impeccable pipeline engineering before training any predictive model.",
        },
        {
          title: "03 / ROI-Driven Approach",
          text: "We do not build technology just for the sake of innovation. Every project at Vidra is designed with clear commercial KPIs agreed from day one.",
        },
      ],
    },
    values: {
      eyebrow: "Our way of working",
      title: "Principles that hold every project together.",
      items: [
        { title: "Talent", text: "We bring technical, strategic, and creative perspectives together to solve problems from multiple angles." },
        { title: "Dedication", text: "We care about delivery, detail, and the real adoption of each solution." },
        { title: "Impartiality", text: "We recommend what the business needs, not what sounds most impressive in a demo." },
      ],
    },
    people: {
      eyebrow: "Our people",
      title: "A team of rigorous experts, focused on delivering operational and high-impact AI solutions.",
      text: "Our team combines diverse expertise and a collaborative culture, focused on maximizing the performance and applicability of every AI solution for our clients.",
      cta: "Explore careers",
      mindsetEyebrow: "How we build it",
        mindset: {
            strategy: {
            title: "ML Inference",
            text: "LSTM, CatBoost, and LightGBM models deployed as synchronous APIs with confidence intervals, trained on real historical client data.",
            },
            technology: {
            title: "Agentic flows",
            text: "Asynchronous multi-agent pipelines with Gemini AI for automated detection, analysis, and scoring of market information.",
            },
            automation: {
            title: "RAG & chatbots",
            text: "Chatbots over a client's own documentation using pgvector, hybrid vector + lexical search, and OpenAI.",
            },
            partnership: {
            title: "Modular platforms",
            text: "Extensible React + Vite + FastAPI + Docker + Electron hubs organised by department, built to grow without rewrites.",
            },
        },
    },
    addValue: {
        title: "What we build",
        description: "Three types of system already in production for our clients.",
        digitaltransformation: {
          title: "Predictive ML models",
          text: "Construction cost estimation with LSTM + CatBoost + LightGBM, trained on real historical data and deployed as APIs with confidence intervals.",
        },
        aiImplementation: {
          title: "Agentic pipelines",
          text: "Automated weekly detection of private tender opportunities via multi-agent analysis with Gemini AI, delivering scored results with 0–100 ranking and commercial feedback.",
        },
        dataStrategy: {
          title: "Modular AI platforms",
          text: "Extensible hubs (React + Vite + FastAPI + Docker + Electron) organized by department. Adding a new feature means editing a configuration registry, not a rewrite.",
        },
    },
    journey: {
        eyebrow: "Our process",
        title: "Designed to turn technical complexity into operational progress.",
        steps: {
            understand: {
            number: "01",
            text: "We understand the context, goals and real constraints of the business.",
            },
            identify: {
            number: "02",
            text: "We identify opportunities where AI can create measurable value.",
            },
            design: {
            number: "03",
            text: "We design practical, scalable solutions aligned with existing teams.",
            },
            implement: {
            number: "04",
            text: "We support execution so transformation reaches day-to-day operations.",
            },
        },
    },
    finalCta: {
        eyebrow: "Let’s talk",
        title: "Ready to transform complexity",
        highlight: "into opportunity?",
        text: "Let’s discuss your next challenge and explore how we can help turn ambition into measurable progress.",
        linkLabel: "Contact us",
    },
  },
} as const;

export const contactPageContent = {
  es: {
    title: "Contacto | Hablemos de tu Proyecto de IA | Vidra",
    description: "¿Tienes un reto con tus datos? Contacta con Vidra para definir el alcance y las prioridades de tu próxima iniciativa de inteligencia artificial.",
    hero: {
      eyebrow: "Contacto",
      title: "Empieza hoy tu próximo proyecto de IA.",
      text: "Tanto si tienes preguntas como si necesitas ayuda personalizada, nuestro equipo está preparado para ayudarte a definir el camino más práctico.",
    },
    officeEyebrow: "Dónde encontrarnos",
    officesTitle: "Todas las oficinas",
    office: {
      city: "Sevilla",
      addressName: "Dirección",
      address: "Calle Américo Vespucio, 5, B-2, 2ª planta. 41092 - Sevilla",
      phoneLabel: "Consultas generales",
      phone: "(+34) 955 023 256",
      emailLabel: "Email",
      email: "contacto@vidra-ia.com",
      mapsLabel: "Abrir en Google Maps",
      mapsHref: "https://www.google.com/maps/search/?api=1&query=Calle%20Am%C3%A9rico%20Vespucio%205%2041092%20Sevilla",
      emailCta: "Contactar por email",
      phoneCta: "Llamar a la oficina",
    },
  },
  en: {
    title: "Contact | Discuss Your Next AI Project | Vidra",
    description: "Evaluating an AI initiative? Get in touch with Vidra to define the scope and practical path forward for your data strategy.",
    hero: {
      eyebrow: "Contact",
      title: "Start your next AI project today.",
      text: "Whether you have questions or need personalized assistance, our team is here to help you define the most practical path forward.",
    },
    officeEyebrow: "Where to find us",
    officesTitle: "All offices",
    office: {
      city: "Sevilla",
      addressName: "Address",
      address: "Calle Américo Vespucio, 5, B-2, 2ª planta. 41092 - Sevilla",
      phoneLabel: "General enquiries",
      phone: "(+34) 955 023 256",
      emailLabel: "Email",
      email: "contacto@vidra-ia.com",
      mapsLabel: "Open in Google Maps",
      mapsHref: "https://www.google.com/maps/search/?api=1&query=Calle%20Am%C3%A9rico%20Vespucio%205%2041092%20Sevilla",
      emailCta: "Get in touch via email",
      phoneCta: "Phone office",
    },
  },
} as const;

export const legalPageContent = {
  es: {
    title: "Legal | Vidra",
    description: "Política de privacidad, términos de uso e información legal de Vidra.",
    heading: "Legal",
    effectiveDate: "Fecha efectiva: 23 de junio de 2026",
    intro: "En Vidra nos tomamos muy en serio tu privacidad y la seguridad de tu información. Esta página resume nuestras políticas sobre recopilación, uso y tratamiento de datos personales.",
    onThisPage: "En esta página",
    sections: [
      {
        id: "privacy",
        title: "Política de privacidad",
        blocks: [
          {
            heading: "Datos personales que recopilamos",
            paragraphs: [
              "Cuando visitas nuestro sitio web, podemos recopilar cierta información sobre tu dispositivo y actividad de navegación.",
            ],
            bullets: [
              "Información del dispositivo: navegador, sistema operativo, dirección IP, identificadores del dispositivo y actividad de navegación.",
              "Datos de uso: páginas vistas, tiempo en el sitio, enlaces pulsados y términos de búsqueda.",
              "Información de contacto: nombre, email, teléfono y contenido del mensaje si contactas con nosotros.",
            ],
          },
          {
            heading: "Cómo usamos tus datos",
            paragraphs: ["Usamos los datos personales recopilados para operar y mejorar el sitio, personalizar la experiencia, analizar el uso, responder consultas y cumplir obligaciones legales."],
          },
          {
            heading: "Base jurídica del tratamiento",
            paragraphs: ["El tratamiento de tus datos personales se fundamenta en las siguientes bases del Art. 6 del RGPD:"],
            bullets: [
              "Consentimiento (Art. 6.1.a): para el uso de cookies analíticas o comunicaciones de marketing, cuando lo hayas otorgado explícitamente.",
              "Ejecución de contrato o medidas precontractuales (Art. 6.1.b): para gestionar consultas, propuestas o contratos de servicios.",
              "Interés legítimo (Art. 6.1.f): para la seguridad, el funcionamiento y la mejora continua del sitio web.",
              "Obligación legal (Art. 6.1.c): cuando la ley nos exige conservar o tratar determinados datos.",
            ],
          },
          {
            heading: "Compartir datos personales",
            paragraphs: ["Podemos compartir datos con proveedores que nos ayudan a operar el sitio y prestar servicios. Estos proveedores deben mantener la información confidencial y segura."],
          },
          {
            heading: "Retención de datos",
            paragraphs: [
              "Conservamos los datos personales durante el tiempo necesario para cumplir las finalidades para las que fueron recopilados o según exija la ley.",
              "Los mensajes enviados al asistente virtual (chatbot) se procesan en tiempo real para generar la respuesta y no se almacenan en nuestros servidores. El historial de conversación se mantiene únicamente en la memoria temporal del navegador durante la sesión activa y se elimina automáticamente al cerrar o recargar la página.",
            ],
          },
          {
            heading: "Tus derechos (ARCO+)",
            paragraphs: ["En virtud del RGPD y la Ley Orgánica 3/2018 (LOPDGDD), tienes los siguientes derechos sobre tus datos personales:"],
            bullets: [
              "Acceso: obtener confirmación de si tratamos tus datos y acceder a ellos.",
              "Rectificación: corregir datos inexactos o incompletos.",
              "Supresión (derecho al olvido): solicitar la eliminación cuando ya no sean necesarios o retires el consentimiento.",
              "Oposición: oponerte al tratamiento cuando se base en interés legítimo o fines de mercadotecnia.",
              "Limitación del tratamiento: restringir el uso de tus datos en determinados supuestos.",
              "Portabilidad: recibir tus datos en formato estructurado, de uso común y lectura mecánica.",
              "No ser objeto de decisiones automatizadas: no ser sometido a decisiones basadas exclusivamente en tratamiento automatizado que te afecten significativamente.",
              "Para ejercer cualquiera de estos derechos, escríbenos a contacto@vidra-ia.com indicando claramente tu solicitud y adjuntando una copia de tu documento de identidad.",
            ],
          },
          {
            heading: "Reclamación ante la autoridad de control",
            paragraphs: ["Si consideras que el tratamiento de tus datos personales no cumple la normativa aplicable, tienes derecho a presentar una reclamación ante la Agencia Española de Protección de Datos (AEPD), con sede en C/ Jorge Juan 6, 28001 Madrid. Más información en www.aepd.es."],
          },
          {
            heading: "Cookies",
            paragraphs: ["Usamos cookies propias y de terceros para recordar preferencias y analizar el uso del sitio. Puedes gestionar tu consentimiento mediante el banner de cookies que aparece al acceder al sitio o desactivarlas desde la configuración de tu navegador."],
          },
        ],
      },
      {
        id: "terms",
        title: "Términos de uso",
        blocks: [
          {
            heading: "Propiedad del contenido",
            paragraphs: ["El contenido del sitio, incluidos textos, gráficos, imágenes, logotipos y otros materiales, pertenece a Vidra o sus licenciantes."],
          },
          {
            heading: "Conducta del usuario",
            paragraphs: ["Aceptas utilizar el sitio de forma legal y respetuosa, sin interferir con su funcionamiento, transmitir código dañino o infringir derechos de terceros."],
          },
          {
            heading: "Descargo de responsabilidad",
            paragraphs: ["La información del sitio se proporciona con fines informativos y no constituye asesoramiento profesional. El uso de la información se realiza bajo tu propio criterio."],
          },
          {
            heading: "Limitación de responsabilidad",
            paragraphs: ["No seremos responsables de daños derivados del uso del sitio, incluidos daños directos, indirectos, incidentales, consecuentes o punitivos."],
          },
          {
            heading: "Ley aplicable",
            paragraphs: ["Estos términos se regirán e interpretarán de acuerdo con la legislación aplicable."],
          },
        ],
      },
      {
        id: "contact-us",
        title: "Contacto",
        blocks: [
          {
            heading: "Contacta con nosotros",
            paragraphs: ["Si tienes preguntas sobre esta política o estos términos, visita la página de contacto o escríbenos a contacto@vidra-ia.com."],
          },
        ],
      },
    ],
  },
  en: {
    title: "Legal | Vidra",
    description: "Vidra privacy policy, terms of use, and legal information.",
    heading: "Legal",
    effectiveDate: "Effective date: June 23, 2026",
    intro: "At Vidra, we take your privacy and the security of your information very seriously. This page outlines our policies regarding the collection, use, and disclosure of personal data.",
    onThisPage: "On this page",
    sections: [
      {
        id: "privacy",
        title: "Privacy Policy",
        blocks: [
          {
            heading: "Personal Data We Collect",
            paragraphs: [
              "When you visit our website, we may collect certain information about your device and browsing activity.",
            ],
            bullets: [
              "Device information: browser type, operating system, IP address, device identifiers, and browsing activity.",
              "Usage data: pages you viewed, time spent on the website, links clicked, and search terms used.",
              "Contact information: name, email address, phone number, and message content if you contact us.",
            ],
          },
          {
            heading: "How We Use Your Personal Data",
            paragraphs: ["We use the personal data we collect to operate and improve our website, personalize your experience, analyze usage, respond to inquiries, and comply with legal obligations."],
          },
          {
            heading: "Legal Basis for Processing",
            paragraphs: ["The processing of your personal data is based on the following grounds under Art. 6 of the GDPR:"],
            bullets: [
              "Consent (Art. 6.1.a): for the use of analytics cookies or marketing communications, where you have given your explicit consent.",
              "Contract or pre-contractual measures (Art. 6.1.b): to handle inquiries, proposals, or service agreements.",
              "Legitimate interest (Art. 6.1.f): for the security, operation, and continuous improvement of our website.",
              "Legal obligation (Art. 6.1.c): where law requires us to retain or process certain data.",
            ],
          },
          {
            heading: "Sharing Your Personal Data",
            paragraphs: ["We may share personal data with third-party service providers who help us operate our website and deliver our services. These providers are required to keep your information confidential and secure."],
          },
          {
            heading: "Data Retention",
            paragraphs: [
              "We retain personal data for as long as necessary to fulfill the purposes for which it was collected, or as required by law.",
              "Messages sent to our virtual assistant (chatbot) are processed in real time to generate a response and are not stored on our servers. Conversation history is held only in the browser's temporary memory during the active session and is automatically deleted when the page is closed or refreshed.",
            ],
          },
          {
            heading: "Your Rights (GDPR)",
            paragraphs: ["Under the General Data Protection Regulation (GDPR) and, where applicable, the Spanish Organic Law 3/2018 (LOPDGDD), you have the following rights:"],
            bullets: [
              "Access: obtain confirmation of whether we process your data and access it.",
              "Rectification: correct inaccurate or incomplete data.",
              "Erasure (right to be forgotten): request deletion when data is no longer necessary or you withdraw consent.",
              "Objection: object to processing where it is based on legitimate interest or for direct marketing purposes.",
              "Restriction: limit how we use your data in certain circumstances.",
              "Portability: receive your data in a structured, commonly used, and machine-readable format.",
              "Not to be subject to automated decision-making: not to be subject to decisions based solely on automated processing that significantly affects you.",
              "To exercise any of these rights, email us at contacto@vidra-ia.com clearly describing your request and attaching a copy of your identity document.",
            ],
          },
          {
            heading: "Right to Lodge a Complaint",
            paragraphs: ["If you believe the processing of your personal data does not comply with applicable law, you have the right to lodge a complaint with the Spanish Data Protection Authority (AEPD), located at C/ Jorge Juan 6, 28001 Madrid. More information at www.aepd.es."],
          },
          {
            heading: "Cookies",
            paragraphs: ["We use first-party and third-party cookies to remember preferences and analyse website usage. You can manage your consent through the cookie banner shown when you first visit the site, or disable cookies in your browser settings."],
          },
        ],
      },
      {
        id: "terms",
        title: "Terms of Use",
        blocks: [
          {
            heading: "Content Ownership",
            paragraphs: ["The content on the website, including text, graphics, images, logos, and other materials, is the property of Vidra or its licensors."],
          },
          {
            heading: "User Conduct",
            paragraphs: ["You agree to use the website in a lawful and respectful manner, without disrupting the website, transmitting harmful code, or infringing third-party rights."],
          },
          {
            heading: "Disclaimer",
            paragraphs: ["The information on the website is provided for informational purposes only and does not constitute professional advice. You rely on it at your own risk."],
          },
          {
            heading: "Limitation of Liability",
            paragraphs: ["We will not be liable for damages arising out of your use of the website, including direct, indirect, incidental, consequential, or punitive damages."],
          },
          {
            heading: "Governing Law",
            paragraphs: ["These terms will be governed by and construed in accordance with applicable law."],
          },
        ],
      },
      {
        id: "contact-us",
        title: "Contact Us",
        blocks: [
          {
            heading: "Contact Us",
            paragraphs: ["If you have any questions about this policy or these terms, please visit our contact page or contact us at contacto@vidra-ia.com."],
          },
        ],
      },
    ],
  },
} as const;

export const footerContent = {
  es: {
    tagline: "Transformamos datos en decisiones inteligentes.",
    social: {
      linkedinLabel: "LinkedIn",
      instagramLabel: "Instagram",
    },
  },
  en: {
    tagline: "We turn data into intelligent decisions.",
    social: {
      linkedinLabel: "LinkedIn",
      instagramLabel: "Instagram",
    },
  },
} as const;

export const footerCopy = {
  es: {
    yearLabel: "© {year} Vidra IA Simply Intelligent SL. Todos los derechos reservados.",
    tagline: "Consultoría en IA para estrategia, entrega e impacto medible.",
    legal: "Legal",
  },
  en: {
    yearLabel: "© {year} Vidra. All rights reserved.",
    tagline: "AI consulting for strategy, delivery, and measurable impact.",
    legal: "Legal",
  },
} as const;

export const searchPageContent = {
  es: {
    title: "Búsqueda | Vidra",
    description: "Resultados de búsqueda en Vidra",
    eyebrow: "Búsqueda",
    emptyTitle: "No se ha encontrado ningún resultado",
    emptyText: "No hemos encontrado resultados para",
    homeLabel: "Volver al inicio",
  },
  en: {
    title: "Search | Vidra",
    description: "Search results at Vidra",
    eyebrow: "Search",
    emptyTitle: "No results found",
    emptyText: "We couldn’t find any results for",
    homeLabel: "Back to home",
  },
} as const;

export const blogPageContent = {
  es: {
    title: "Blog sobre IA y Estrategia de Datos | Vidra",
    heading: "Blog sobre IA y Estrategia de Datos",
    description: "Análisis, guías y casos de estudio sobre la implementación de Inteligencia Artificial en el entorno empresarial.",
    eyebrow: "Nuestro Blog",
    empty: "No hay artículos publicados todavía.",
    readMore: "Leer artículo",
    backToBlog: "Volver al blog",
    categories: {
      analytics: "Analytics",
      "machine-learning": "Machine Learning",
      "deep-learning": "Deep Learning",
    },
    ctaBlock: {
      title: "¿Evaluando una iniciativa similar?",
      description: "Podemos ayudarte a definir el alcance y la ruta técnica más práctica para tu proyecto de IA.",
      cta: "Hablemos de tu proyecto"
    }
  },
  en: {
    title: "AI & Data Strategy Blog | Vidra",
    heading: "AI & Data Strategy Blog",
    description: "Insights, guides, and case studies on implementing Artificial Intelligence for business impact.",
    eyebrow: "Our Blog",
    empty: "No articles published yet.",
    readMore: "Read article",
    backToBlog: "Back to blog",
    categories: {
      analytics: "Analytics",
      "machine-learning": "Machine Learning",
      "deep-learning": "Deep Learning",
    },
    ctaBlock: {
      title: "Evaluating a similar initiative?",
      description: "We can help you define the scope and most practical technical path for your AI project.",
      cta: "Let's discuss your project"
    }
  },
} as const;

export const projectsContent = {
  es: {
    title: "Proyectos | Vidra IA",
    description: "Proyectos reales de inteligencia artificial desarrollados por Vidra para empresas del sector construcción e industria.",
    eyebrow: "Proyectos",
    heading: "IA que ya está en producción.",
    subheading: "Cada proyecto nace de un problema concreto. Estos son los sistemas que hemos construido y desplegado para nuestros clientes.",
    allLabel: "Ver todos",
    techLabel: "Tecnologías",
    statusLabel: "Estado",
    statusValues: {
      enPruebas: "En pruebas",
      enDesarrollo: "En desarrollo",
      finalizado: "Finalizado",
    },
    projects: [
      {
        id: "argenia-hub",
        client: "Argenia",
        title: "Argenia Hub — Estimador de presupuestos con ML",
        description: "Hub extensible de herramientas de IA para el sector de la construcción. El módulo activo estima el coste de partidas de obra mediante modelos LSTM + CatBoost entrenados con histórico real de presupuestos.",
        outcome: "Predicciones con intervalos de confianza sobre ficheros Excel de partidas de obra. Disponible como app web y de escritorio (Electron).",
        status: "enPruebas",
        stack: ["LSTM", "CatBoost", "LightGBM", "React + Vite", "FastAPI", "PostgreSQL", "Docker"],
        category: "ml",
        url: "https://argenia.vidra-ia.com",
      },
      {
        id: "area-hub",
        client: "Area Construcción",
        title: "Area Hub — Plataforma IA para constructoras",
        description: "Hub modular de herramientas de inteligencia artificial organizado por departamentos (Estudios, Compras, Producción). Diseñado para crecer: añadir una nueva funcionalidad es editar un registro de configuración.",
        outcome: "Aplicación web con acceso restringido por IP desplegada en producción. App de escritorio (Electron) con auto-actualización silenciosa.",
        status: "enDesarrollo",
        stack: ["React + Vite", "FastAPI", "PostgreSQL", "Docker", "Electron"],
        category: "app",
        url: "https://app.areaconstruccion.vidra-ia.com",
      },
      {
        id: "radar-licitaciones",
        client: "Area Construcción",
        title: "Radar de Licitaciones Privadas",
        description: "Pipeline automático semanal que detecta, analiza y puntúa oportunidades de obra privada de construcción antes de que salgan a licitación pública. Usa IA multi-agente (Gemini) para evaluar cada señal del mercado.",
        outcome: "Newsletter semanal de oportunidades con score 0–100, nivel de certeza y feedback comercial inline. Integrado en Area Hub.",
        status: "enDesarrollo",
        stack: ["Python 3.12", "Gemini AI", "SQLite", "FastAPI", "Pydantic"],
        category: "agentic",
        url: null,
      },
    ],
  },
  en: {
    title: "Projects | Vidra IA",
    description: "Real AI projects developed by Vidra for companies in construction and industry.",
    eyebrow: "Projects",
    heading: "AI already running in production.",
    subheading: "Each project starts with a concrete problem. These are the systems we have built and deployed for our clients.",
    allLabel: "View all",
    techLabel: "Technologies",
    statusLabel: "Status",
    statusValues: {
      enPruebas: "In testing",
      enDesarrollo: "In development",
      finalizado: "Completed",
    },
    projects: [
      {
        id: "argenia-hub",
        client: "Argenia",
        title: "Argenia Hub — ML Budget Estimator",
        description: "Extensible AI hub for the construction sector. The active module estimates work item costs using LSTM + CatBoost models trained on real historical budget data.",
        outcome: "Predictions with confidence intervals over Excel work item files. Available as both web and desktop app (Electron).",
        status: "enPruebas",
        stack: ["LSTM", "CatBoost", "LightGBM", "React + Vite", "FastAPI", "PostgreSQL", "Docker"],
        category: "ml",
        url: "https://argenia.vidra-ia.com",
      },
      {
        id: "area-hub",
        client: "Area Construcción",
        title: "Area Hub — AI Platform for Construction",
        description: "Modular AI hub organised by departments (Studies, Procurement, Production). Designed to grow: adding a new feature means editing a configuration registry.",
        outcome: "IP-restricted web application deployed in production. Desktop app (Electron) with silent auto-update.",
        status: "enDesarrollo",
        stack: ["React + Vite", "FastAPI", "PostgreSQL", "Docker", "Electron"],
        category: "app",
        url: "https://app.areaconstruccion.vidra-ia.com",
      },
      {
        id: "radar-licitaciones",
        client: "Area Construcción",
        title: "Private Tender Radar",
        description: "Automated weekly pipeline that detects, analyses, and scores private construction opportunities before they go to public tender. Uses multi-agent AI (Gemini) to evaluate each market signal.",
        outcome: "Weekly opportunity newsletter with 0–100 score, certainty level, and inline commercial feedback. Integrated into Area Hub.",
        status: "enDesarrollo",
        stack: ["Python 3.12", "Gemini AI", "SQLite", "FastAPI", "Pydantic"],
        category: "agentic",
        url: null,
      },
    ],
  },
} as const;

export const teamContent = {
  es: {
    eyebrow: "Equipo",
    title: "Las personas que hacen el trabajo.",
    description: "Combinamos experiencia en ciencia de datos, ingeniería de software y gestión de proyectos para entregar sistemas de IA que funcionan en producción.",
    members: [
      { initials: "JM", name: "Jose Antonio Morales", role: "Socio", area: "Dirección y estrategia" },
      { initials: "JB", name: "Jorge Bernal", role: "Socio", area: "Dirección y operaciones" },
      { initials: "JS", name: "Juan Sánchez", role: "Socio", area: "Dirección comercial" },
      { initials: "IN", name: "Ignacio Navoz", role: "Responsable técnico", area: "Arquitectura y MLOps" },
      { initials: "JC", name: "Javier Cerón", role: "Ingeniero IA", area: "Desarrollo e infraestructura" },
      { initials: "AC", name: "Álvaro Carrera", role: "Ingeniero IA", area: "Modelos y backend" },
      { initials: "CD", name: "Carlos Díaz", role: "Ingeniero IA", area: "Frontend y despliegue" },
      { initials: "GH", name: "Gonzalo Humanes", role: "Ingeniero IA", area: "Análisis y modelos" },
    ],
  },
  en: {
    eyebrow: "Team",
    title: "The people who do the work.",
    description: "We combine expertise in data science, software engineering, and project management to deliver AI systems that run in production.",
    members: [
      { initials: "JM", name: "Jose Antonio Morales", role: "Partner", area: "Direction & strategy" },
      { initials: "JB", name: "Jorge Bernal", role: "Partner", area: "Direction & operations" },
      { initials: "JS", name: "Juan Sánchez", role: "Partner", area: "Commercial direction" },
      { initials: "IN", name: "Ignacio Navoz", role: "Technical lead", area: "Architecture & MLOps" },
      { initials: "JC", name: "Javier Cerón", role: "AI Engineer", area: "Development & infrastructure" },
      { initials: "AC", name: "Álvaro Carrera", role: "AI Engineer", area: "Models & backend" },
      { initials: "CD", name: "Carlos Díaz", role: "AI Engineer", area: "Frontend & deployment" },
      { initials: "GH", name: "Gonzalo Humanes", role: "AI Engineer", area: "Analytics & models" },
    ],
  },
} as const;

export const clientsContent = {
  es: {
    eyebrow: "Empresas con las que hemos trabajado",
    clients: [
      { name: "Argenia", sector: "Construcción e ingeniería" },
      { name: "Area Construcción", sector: "Construcción" },
    ],
  },
  en: {
    eyebrow: "Companies we have worked with",
    clients: [
      { name: "Argenia", sector: "Construction & engineering" },
      { name: "Area Construcción", sector: "Construction" },
    ],
  },
} as const;
