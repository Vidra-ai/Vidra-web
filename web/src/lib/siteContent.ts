export type Locale = "es" | "en";

export const localeLinks = {
  es: {
    switchLabel: "EN",
    switchHref: "/en",
    nav: [
      { label: "Qué hacemos", href: "/#what-we-do" },
      { label: "Procesos", href: "/#process" },
      { label: "Quiénes somos", href: "/#who-we-are" },
      { label: "Contacto", href: "/#contact" },
      { label: "Blog", href: "/blog" },
      { label: "Asistente", href: "/chat" },
    ],
    footer: [
      { label: "Qué hacemos", href: "/#what-we-do" },
      { label: "Procesos", href: "/#process" },
      { label: "Quiénes somos", href: "/#who-we-are" },
      { label: "Contacto", href: "/contact" },
      { label: "Blog", href: "/blog" },
      { label: "Asistente", href: "/chat" },
    ],
  },
  en: {
    switchLabel: "ES",
    switchHref: "/",
    nav: [
      { label: "What we do", href: "/en/#what-we-do" },
      { label: "Process", href: "/en/#process" },
      { label: "Who we are", href: "/en/#who-we-are" },
      { label: "Contact", href: "/en/#contact" },
      { label: "Blog", href: "/en/blog" },
      { label: "Assistant", href: "/en/chat" },
    ],
    footer: [
      { label: "What we do", href: "/en/#what-we-do" },
      { label: "Process", href: "/en/#process" },
      { label: "Who we are", href: "/en/#who-we-are" },
      { label: "Contact", href: "/en/#contact" },
      { label: "Blog", href: "/en/blog" },
      { label: "Assistant", href: "/en/chat" },
    ],
  },
} as const;

export const homeContent = {
  es: {
    title: "Vidra | Consultoría de IA y Estrategia de Datos para Empresas",
    description: "Expertos en soluciones de IA: Auditoría de datos, modelos predictivos y Deep Learning. Transformamos información compleja en resultados de negocio medibles.",
    hero: {
      description: "Convertimos la información de negocio en sistemas de IA listos para operar y fáciles de adoptar.",
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
            alt: "Persona trabajando con datos en un portátil",
        },
        {
            label: "Motor predictivo",
            title: "Modelos predictivos de machine learning",
            description: "Desarrollamos modelos a medida para anticipar riesgos, prever demanda y apoyar mejores decisiones operativas.",
            imageKey: "machineLearning-hero",
            alt: "Equipo revisando paneles de analítica predictiva",
        },
        {
            label: "Redes neuronales",
            title: "IA avanzada para datos complejos",
            description: "Aplicamos deep learning a lenguaje, imágenes y patrones difíciles de resolver con enfoques tradicionales.",
            imageKey: "deepLearning-hero",
            alt: "Visualización abstracta de redes neuronales y datos",
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
          title: "Deep Learning",
          description: "Diseñamos modelos avanzados para desafíos visuales, textuales y de datos no estructurados.",
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
      description: "We turn raw business information into operational AI systems that are ready to use and easy to adopt.",
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
        alt: "Person working with data on a laptop",
        },
        {
        label: "Predictive engine",
        title: "Predictive machine learning models",
        description: "We build tailored models to anticipate risk, forecast demand, and support better operational decisions.",
        imageKey: "machineLearning-hero",
        alt: "Team reviewing predictive analytics dashboards",
        },
        {
        label: "Neural networks",
        title: "Advanced AI for complex data",
        description: "We apply deep learning to language, images, and patterns that are difficult to solve with traditional approaches.",
        imageKey: "deepLearning-hero",
        alt: "Abstract visualization of neural networks and data",
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
          title: "Deep Learning",
          description: "Design advanced models for complex visual, textual, and unstructured data challenges.",
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
        metaDescription: "Desarrollo de sistemas predictivos personalizados para previsión de demanda, riesgos y automatización inteligente.",
        slug: "machine-learning",
        eyebrow: "Servicio 02",
        imageKey: "machineLearning",
        description: "Diseñamos y desplegamos sistemas predictivos que ayudan a automatizar decisiones, mejorar previsiones y actuar sobre datos complejos.",
        points: ["Modelado predictivo", "Sistemas de recomendación", "Evaluación y despliegue de modelos"],
      },
      {
        title: "Deep Learning",
        metaTitle: "Soluciones de Deep Learning y Redes Neuronales | Vidra",
        metaDescription: "IA avanzada para procesamiento de lenguaje natural (NLP), visión por computador y datos no estructurados.",
        slug: "deep-learning",
        eyebrow: "Servicio 03",
        imageKey: "deepLearning",
        description: "Construimos soluciones avanzadas de IA para datos complejos como lenguaje, imágenes, documentos y patrones de comportamiento a gran escala.",
        points: ["Procesamiento de lenguaje natural", "Visión por computador", "Optimización de redes neuronales"],
      },
    ],
    detail: {
      analysis: {
        title: "Análisis",
        eyebrow: "Servicio 01",
        description: "Ayudamos a las organizaciones a entender su entorno de datos, identificar oportunidades de alto impacto y definir una hoja de ruta práctica antes de invertir en la ejecución.",
        heroImageKey: "analysis-hero",
        points: [
          "Evaluación de oportunidades de negocio y datos",
          "Definición de KPI y medición de éxito",
          "Revisión de calidad, disponibilidad y madurez de datos",
          "Priorización de casos de uso según impacto",
        ],
      },
      "machine-learning": {
        title: "Machine Learning",
        eyebrow: "Servicio 02",
        description: "Diseñamos, entrenamos y desplegamos modelos de machine learning que convierten datos operativos en predicciones, recomendaciones y decisiones asistidas.",
        heroImageKey: "machineLearning-hero",
        points: [
          "Modelado predictivo y forecasting",
          "Clasificación, scoring y recomendación",
          "Evaluación de modelos y mejora de rendimiento",
          "Flujos de trabajo listos para despliegue",
        ],
      },
      "deep-learning": {
        title: "Deep Learning",
        eyebrow: "Servicio 03",
        description: "Construimos sistemas avanzados con deep learning para tareas complejas que involucran lenguaje, imágenes, patrones y datos no estructurados a gran escala.",
        heroImageKey: "deepLearning-hero",
        points: [
          "Soluciones de procesamiento de lenguaje natural",
          "Visión por computador e inteligencia visual",
          "Diseño de arquitecturas de redes neuronales",
          "Entrenamiento y optimización avanzada",
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
        metaTitle: "Predictive Machine Learning Solutions | Vidra",
        metaDescription: "Tailored predictive systems to anticipate risks, forecast demand, and support data-driven decision making.",
        slug: "machine-learning",
        eyebrow: "Service 02",
        imageKey: "machineLearning",
        description: "We design and deploy predictive systems that help teams automate decisions, improve forecasting, and act on complex data.",
        points: ["Predictive modelling", "Recommendation systems", "Model evaluation and deployment"],
      },
      {
        title: "Deep Learning",
        metaTitle: "Advanced Deep Learning & Neural Networks | Vidra",
        metaDescription: "Custom AI for NLP, computer vision, and large-scale unstructured data challenges.",
        slug: "deep-learning",
        eyebrow: "Service 03",
        imageKey: "deepLearning",
        description: "We build advanced AI solutions for complex data such as language, images, documents, and large-scale behavioural patterns.",
        points: ["Natural language processing", "Computer vision", "Neural network optimisation"],
      },
    ],
    detail: {
      analysis: {
        title: "Analysis",
        eyebrow: "Service 01",
        description: "We help organizations understand their data landscape, identify high-impact opportunities, and define a practical roadmap before committing resources to implementation.",
        heroImageKey: "analysis-hero",
        points: [
          "Business and data opportunity assessment",
          "KPI definition and success measurement",
          "Data quality, availability, and readiness review",
          "Use case prioritization based on business impact",
        ],
      },
      "machine-learning": {
        title: "Machine Learning",
        eyebrow: "Service 02",
        description: "We design, train, and deploy machine learning models that transform operational data into predictions, recommendations, and automated decision support.",
        heroImageKey: "machineLearning-hero",
        points: [
          "Predictive modelling and forecasting",
          "Classification, scoring, and recommendation systems",
          "Model evaluation and performance improvement",
          "Deployment-ready ML workflows",
        ],
      },
      "deep-learning": {
        title: "Deep Learning",
        eyebrow: "Service 03",
        description: "We build advanced AI systems using deep learning for complex tasks involving language, images, patterns, and large-scale unstructured data.",
        heroImageKey: "deepLearning-hero",
        points: [
          "Natural language processing solutions",
          "Computer vision and image-based intelligence",
          "Neural network architecture design",
          "Advanced model training and optimization",
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
            number: "Enfoque",
            label: "En soluciones aplicables y de impacto inmediato",
        },
        approach: {
            number: "0",
            label: "Dependencia de proveedor",
        },
        expertise: {
            number: "3",
            label: "Áreas principales de especialización",
        },
        independence: {
            number: "100%",
            label: "Asesoría independiente y objetiva",
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
    testimonial: {
      eyebrow: "Palabras de clientes",
      quote: "Vidra nos ayudó a mejorar de forma significativa nuestro proceso de due diligence técnico, elevando la claridad de las decisiones y la protección ante riesgos.",
      author: "John Doe",
      role: "Development Manager, Acme Corp.",
    },
    people: {
      eyebrow: "Nuestro equipo",
      title: "Expertos en datos, IA y estrategia aplicada.",
      text: "Combinamos perfiles técnicos y estratégicos para diseñar soluciones de IA que puedan integrarse en la operativa real del negocio.",
      cta: "Explorar carreras",
      cards: [
        { title: "Careers", text: "Únete a un equipo que trabaja en IA aplicada a problemas reales.", href: "/#contact" },
        { title: "What we do", text: "Descubre cómo convertimos datos en sistemas operativos y medibles.", href: "/#what-we-do" },
        { title: "Insights", text: "Lee análisis sobre tendencias, implementación y toma de decisiones." },
        { title: "Projects", text: "Explora proyectos donde estrategia, datos e ingeniería se encuentran."},
      ],
      mindsetEyebrow: "Mentalidad de liderazgo",
        mindset: {
        strategy: {
            title: "Estrategia de negocio",
            text: "Alineamos iniciativas de transformación con resultados de negocio medibles.",
        },
        technology: {
            title: "Liderazgo tecnológico",
            text: "Conectamos la visión ejecutiva con la ejecución técnica.",
        },
        automation: {
            title: "IA y automatización",
            text: "Adopción práctica enfocada en eficiencia, crecimiento y uso real.",
        },
        partnership: {
            title: "Colaboración a largo plazo",
            text: "Nos mantenemos cerca más allá de la entrega inicial.",
        },
        },
    },
    addValue: {
        title: "Nuestro valor diferencial",
        description: "Estrategia, tecnología y ejecución para generar resultados tangibles.",
        digitaltransformation: {
          title: "Transformación digital",
          text: "Transformamos ambiciones digitales en planes de acción concretos y resultados medibles.",
        },
        aiImplementation: {
          title: "IA y automatización",
          text: "Identificamos y capitalizamos oportunidades donde la IA genera valor empresarial cuantificable.",
        },
        dataStrategy: {
          title: "Diseño de modelos operativos",
          text: "Diseñamos modelos operativos que alinean equipos, procesos y tecnología para una escalabilidad óptima.",
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
            number: "Focus",
            label: "On actionable solutions with immediate impact",
        },
        approach: {
            number: "0",
            label: "Complete technological independence",
        },
        expertise: {
            number: "3",
            label: "Core areas of expertise", 
        },
        independence: {
            number: "100%",
            label: "100% independent and objective advisory",
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
    testimonial: {
      eyebrow: "Words from our customers",
      quote: "Vidra has helped to improve our technical due diligence process greatly, increasing our protection on deals and outlining risk decisions clearly.",
      author: "John Doe",
      role: "Development Manager, Acme Corp.",
    },
    people: {
      eyebrow: "Our people",
      title: "A team of rigorous experts, focused on delivering operational and high-impact AI solutions.",
      text: "Our team combines diverse expertise and a collaborative culture, focused on maximizing the performance and applicability of every AI solution for our clients.",
      cta: "Explore careers",
      cards: [
        { title: "Careers", text: "Join a team working on AI applied to real operational problems.", href: "/en/#contact" },
        { title: "What we do", text: "See how we turn data into operational, measurable systems.", href: "/en/#what-we-do" },
        { title: "Insights", text: "Read analysis on trends, implementation, and decision-making." },
        { title: "Projects", text: "Explore work where strategy, data, and engineering meet." },
      ],
      mindsetEyebrow: "Leadership mindset",
        mindset: {
            strategy: {
            title: "Business strategy",
            text: "We align transformation initiatives with measurable business outcomes.",
            },
            technology: {
            title: "Technology leadership",
            text: "We bridge executive vision and technical execution.",
            },
            automation: {
            title: "AI & automation",
            text: "Practical adoption focused on efficiency, growth and real-world use.",
            },
            partnership: {
            title: "Long-term partnership",
            text: "We stay involved beyond the initial delivery.",
            },
        },
    },
    addValue: {
        title: "Our Differentiating Value",
        description: "Proven experience integrating strategy, technology, and execution for tangible results.",
        digitaltransformation: {
          title: "Digital transformation",
          text: "We translate digital ambitions into concrete action plans and measurable outcomes.",
        },
        aiImplementation: {
          title: "AI & Automation",
          text: "We identify and capitalize on opportunities where AI generates quantifiable business value.",
        },
        dataStrategy: {
          title: "Operating Model Design",
          text: "We design operating models that align teams, processes, and technology for optimal scalability.",
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
    effectiveDate: "Fecha efectiva: 3 de julio de 2024",
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
            heading: "Compartir datos personales",
            paragraphs: ["Podemos compartir datos con proveedores que nos ayudan a operar el sitio y prestar servicios. Estos proveedores deben mantener la información confidencial y segura."],
          },
          {
            heading: "Retención de datos",
            paragraphs: ["Conservamos los datos personales durante el tiempo necesario para cumplir las finalidades para las que fueron recopilados o según exija la ley."],
          },
          {
            heading: "Tus derechos",
            paragraphs: ["Puedes solicitar acceso, actualización o eliminación de tus datos, así como oponerte a determinados tratamientos."],
          },
          {
            heading: "Cookies",
            paragraphs: ["Usamos cookies para recordar preferencias y entender el uso del sitio. Puedes desactivarlas desde la configuración de tu navegador."],
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
    effectiveDate: "Effective date: July 3, 2024",
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
            heading: "Sharing Your Personal Data",
            paragraphs: ["We may share personal data with third-party service providers who help us operate our website and deliver our services. These providers are required to keep your information confidential and secure."],
          },
          {
            heading: "Data Retention",
            paragraphs: ["We retain personal data for as long as necessary to fulfill the purposes for which it was collected, or as required by law."],
          },
          {
            heading: "Your Rights",
            paragraphs: ["You may request access to, updates to, or deletion of your data, and you may object to certain processing activities."],
          },
          {
            heading: "Cookies",
            paragraphs: ["We use cookies to remember preferences and understand how the website is used. You can disable cookies through your browser settings."],
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
    yearLabel: "© {year} Vidra. Todos los derechos reservados.",
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
