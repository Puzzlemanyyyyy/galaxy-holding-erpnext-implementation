import { DomainCard } from './components/DomainCard';
import { MetricCard } from './components/MetricCard';
import { SectionTitle } from './components/SectionTitle';
import { Timeline } from './components/Timeline';

const metrics = [
  {
    value: '31',
    label: 'Colaboradores',
    caption: 'Distribuidos en estructura multi-dominio con roles estandarizados.'
  },
  {
    value: '12',
    label: 'Semanas',
    caption: 'Plan maestro de implementación simultánea de ERP, automatización e IA.'
  },
  {
    value: '95%',
    label: 'Automatización',
    caption: 'Reducción del esfuerzo manual en reportes ejecutivos y facturación intercompañía.'
  },
  {
    value: '7',
    label: 'Dominios',
    caption: 'Expansión preparada para nuevas unidades de negocio y servicios especializados.'
  }
];

const activeDomains = [
  {
    name: 'Galaxy Holding',
    teamSize: '16 personas · Dirección, administración, TI y operaciones',
    focus: ['Gobierno corporativo', 'Finanzas consolidadas', 'TI y seguridad', 'Estrategia'],
    status: 'Activo' as const
  },
  {
    name: 'Galaxy Bio',
    teamSize: '9 personas · Ingeniería bio y biotecnología',
    focus: ['Gestión de laboratorios', 'Trazabilidad', 'Control de calidad', 'Proyectos I+D'],
    status: 'Activo' as const
  },
  {
    name: 'Galaxy Software',
    teamSize: '6 personas · Ingeniería de software y analítica',
    focus: ['Desarrollo ágil', 'Integraciones API', 'Análisis de datos', 'Servicios cloud'],
    status: 'Activo' as const
  }
];

const expansionDomains = [
  {
    name: 'Galaxy Pay',
    teamSize: 'Fintech & pagos digitales',
    focus: ['Onboarding regulatorio', 'Antifraude', 'Plataforma multi-divisa'],
    status: 'Planificado' as const
  },
  {
    name: 'Galaxy Financial',
    teamSize: 'Consultoría financiera especializada',
    focus: ['Gestión patrimonial', 'Due diligence', 'Inteligencia de riesgos'],
    status: 'Planificado' as const
  },
  {
    name: 'Asterion Capital',
    teamSize: 'Gestión de inversiones',
    focus: ['Fondos de capital', 'Estructuración de deals', 'Gobierno de portafolio'],
    status: 'Planificado' as const
  },
  {
    name: 'Sygma Insurance',
    teamSize: 'Seguros especializados',
    focus: ['Suscripción técnica', 'Gestión de pólizas', 'Atención a siniestros'],
    status: 'Planificado' as const
  },
  {
    name: 'Galaxy Tower',
    teamSize: 'Desarrollo inmobiliario',
    focus: ['Gestión de proyectos', 'Contratistas', 'Comercialización'],
    status: 'Planificado' as const
  },
  {
    name: 'Galaxy Engineering',
    teamSize: 'Ingenierías especializadas',
    focus: ['Planificación BIM', 'Control de obra', 'Certificaciones'],
    status: 'Planificado' as const
  },
  {
    name: 'Galaxy Flash',
    teamSize: 'Energías renovables',
    focus: ['Gestión de parques solares', 'Monitoreo IoT', 'Mercado energético'],
    status: 'Planificado' as const
  }
];

const workflows = [
  {
    title: 'Facturación intercompany automática',
    description:
      'Cálculo de fees de management (2% ingresos) y emisión de facturas de compra/venta entre compañías cada 28 días.'
  },
  {
    title: 'Alertas en Microsoft Teams',
    description:
      'Notificaciones en tiempo real para facturas, proyectos y alertas de calidad integradas vía n8n + Webhooks.'
  },
  {
    title: 'Reportes ejecutivos con IA',
    description:
      'Consultas GPT con análisis financiero y operativo conectadas al API de ERPNext para respuestas en español.'
  }
];

const capabilities = [
  {
    title: 'ERPNext Multicompany',
    description:
      'Gestión financiera, compras, proyectos y manufactura con taxonomía común para todas las compañías Galaxy.',
    highlights: ['Plan contable consolidado', 'Centros de costo por dominio', 'Automatización de impuestos', 'Informes IFRS']
  },
  {
    title: 'Automatización n8n',
    description:
      'Workflows orquestados para sincronización con Microsoft 365, Teams y bots internos para soporte operativo.',
    highlights: ['Conectores M365', 'Orquestación de facturación', 'Integración con BI', 'Gestión de incidencias']
  },
  {
    title: 'Asistentes de IA',
    description:
      'Plantillas GPT especializadas para análisis ejecutivo y asistencia técnica con contexto de datos y procesos.',
    highlights: ['Prompting contextual', 'Ingesta de documentación', 'Reportes conversacionales', 'Seguridad y auditoría']
  }
];

const highlights = [
  'Migración lista para deploy en Vercel',
  'Documentación integral de implementación',
  'Scripts de automatización para bootstrap ERPNext',
  'Arquitectura lista para escalar nuevos dominios'
];

export default function HomePage() {
  return (
    <main>
      <section className="hero">
        <div>
          <span className="chip">ERPNext · n8n · IA</span>
          <h1>
            Ecosistema operativo inteligente para <br /> Galaxy Holding
          </h1>
          <p>
            Implementación lista para producción que une ERPNext, automatización n8n y asistentes de inteligencia
            artificial. Diseñado para una estructura multiempresa con expansión a siete dominios adicionales.
          </p>
          <div className="hero-cta">
            <a href="/docs/galaxy_master_document" download>
              Descargar Master Plan
            </a>
            <a className="secondary" href="https://github.com/Puzzlemanyyyyy/galaxy-holding-erpnext-implementation" target="_blank" rel="noreferrer">
              Ver repositorio
            </a>
          </div>
          <div className="metrics-grid">
            {metrics.map((metric) => (
              <MetricCard key={metric.label} {...metric} />
            ))}
          </div>
        </div>
        <div className="card">
          <h3>Arquitectura Convergente</h3>
          <p>
            Infraestructura Dockerizada con ERPNext, n8n, Redis, MariaDB, PostgreSQL y Nginx. Incluye scripts de bootstrap,
            plantillas de workflows y configuraciones listas para despliegue híbrido.
          </p>
          <div className="chip-list">
            {highlights.map((item) => (
              <span className="chip" key={item}>
                {item}
              </span>
            ))}
          </div>
        </div>
      </section>

      <section>
        <SectionTitle
          title="Dominios activos"
          description="Coordinación operativa y financiera para las unidades activas de Galaxy Holding utilizando un core ERP unificado."
        />
        <div className="domains-grid">
          {activeDomains.map((domain) => (
            <DomainCard key={domain.name} {...domain} />
          ))}
        </div>
      </section>

      <section>
        <SectionTitle
          title="Expansión planificada"
          description="Arquitectura preparada para integrar siete dominios adicionales manteniendo gobernanza, cumplimiento y analítica en tiempo real."
        />
        <div className="domains-grid">
          {expansionDomains.map((domain) => (
            <DomainCard key={domain.name} {...domain} />
          ))}
        </div>
      </section>

      <section>
        <SectionTitle
          title="Capacidades del ecosistema"
          description="Componentes técnicos clave que habilitan la operación multiempresa con automatizaciones y asistentes cognitivos."
        />
        <div className="grid-columns-3">
          {capabilities.map((capability) => (
            <article className="card" key={capability.title}>
              <h3>{capability.title}</h3>
              <p>{capability.description}</p>
              <div className="chip-list">
                {capability.highlights.map((highlight) => (
                  <span className="chip" key={highlight}>
                    {highlight}
                  </span>
                ))}
              </div>
            </article>
          ))}
        </div>
      </section>

      <section>
        <SectionTitle
          title="Workflows automatizados"
          description="Procesos orquestados con n8n, Teams y GPT para reducir tiempos de operación y elevar la visibilidad ejecutiva."
          actionLabel="Ver workflows"
          actionHref="/docs/erp_crm_expansion_plan.md"
        />
        <Timeline items={workflows} />
        <div className="badge-grid">
          <span className="badge">Integración M365</span>
          <span className="badge">Automatización financiera</span>
          <span className="badge">Data governance</span>
          <span className="badge">IA aplicada</span>
        </div>
      </section>

      <section>
        <SectionTitle
          title="Lista para despliegue"
          description="Plantillas, scripts y configuraciones revisadas para ejecución inmediata en entornos Docker o despliegues híbridos en la nube."
          actionLabel="Guía de instalación"
          actionHref="/docs/installation_guide.md"
        />
        <div className="grid-columns-3">
          <article className="card">
            <h3>Infraestructura optimizada</h3>
            <p>
              Contenedores ERPNext y n8n configurados con healthchecks, volúmenes persistentes y reverse proxy seguro listo
              para certificados TLS.
            </p>
          </article>
          <article className="card">
            <h3>Bootstrap automatizado</h3>
            <p>
              Scripts Python para crear compañías, roles, permisos y cargas iniciales del CRM, incluyendo conexión con
              Verifactu.
            </p>
          </article>
          <article className="card">
            <h3>Gobernanza y seguridad</h3>
            <p>
              Roles segmentados por dominio, controles de auditoría y guías de integración con Microsoft 365 para autenticación
              centralizada.
            </p>
          </article>
        </div>
      </section>

      <section className="footer">
        <p>© {new Date().getFullYear()} Galaxy Holding. Implementación ERPNext + n8n + IA.</p>
        <a href="mailto:tech@galaxyholding.io">tech@galaxyholding.io</a>
      </section>
    </main>
  );
}
