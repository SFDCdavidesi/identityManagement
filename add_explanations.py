"""
Script para añadir explicaciones detalladas y corregir respuestas
en el banco de preguntas de Salesforce Identity & Access Management.
"""
import json
import os

BASE_DIR = r"C:\Users\david\python\cert-salesforce"

# Corrections: questions where the original answer was wrong
CORRECTIONS = {
    3: {"correct": ["B"]},
    6: {"correct": ["B", "C"]},
    50: {"correct": ["B"]},
    51: {"correct": ["C"]},
}

# Detailed explanations for all 76 questions
EXPLANATIONS = {
    1: {
        "explanation": (
            "La respuesta correcta es D (Just-in-Time Provisioning). "
            "El aprovisionamiento Just-in-Time (JIT) es una funcionalidad nativa de Salesforce que permite crear o actualizar registros de usuario "
            "automáticamente durante el proceso de inicio de sesión SSO mediante SAML. Cuando un usuario se autentica por primera vez a través del IdP externo "
            "y Salesforce recibe la aserción SAML, si JIT está habilitado, Salesforce crea automáticamente el registro de usuario con los atributos "
            "proporcionados en la aserción (nombre, email, perfil, etc.) sin necesidad de que el usuario exista previamente en Salesforce.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (AppExchange): Aunque existen soluciones de terceros, no es la recomendación estándar cuando Salesforce ofrece JIT de forma nativa.\n"
            "- B (Custom middleware): Crear middleware personalizado añade complejidad innecesaria. JIT resuelve este caso sin desarrollo adicional.\n"
            "- C (Custom login flow + Apex handler): Los Login Flows se ejecutan después de la autenticación, no crean usuarios. "
            "Además, requieren desarrollo custom, mientras que JIT es una configuración declarativa.\n\n"
            "JIT provisioning soporta dos modalidades: Standard JIT (usa atributos SAML predefinidos) y Custom JIT (usa una clase Apex que implementa "
            "la interfaz Auth.SamlJitHandler para lógica personalizada). En este escenario, como UC quiere crear usuarios automáticamente en el primer login "
            "SSO, JIT es la solución ideal porque se integra directamente con el flujo SAML existente del IdP de terceros."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.sso_jit_about.htm&type=5"
    },
    2: {
        "explanation": (
            "Las respuestas correctas son B y C. Customer 360 Identity es una solución de Salesforce que proporciona servicios de identidad centralizados "
            "para consumidores y clientes a través de múltiples propiedades digitales.\n\n"
            "B es correcta porque Customer 360 Identity soporta múltiples marcas (multi-brand). Esto significa que una organización puede operar varias "
            "marcas comerciales diferentes, cada una con su propia experiencia de usuario y branding, pero compartiendo un sistema de identidad centralizado. "
            "Esto permite correlacionar la actividad del usuario incluso cuando interactúa con diferentes marcas de la misma empresa.\n\n"
            "C es correcta porque Customer 360 Identity permite construir un login único (single login) para cada cliente, dando a la organización "
            "visibilidad completa de la actividad de inicio de sesión del usuario en todas sus propiedades digitales y aplicaciones. "
            "Esto es fundamental para obtener una vista unificada del cliente.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A: Customer 360 Identity NO rastrea la actividad de usuarios anónimos antes del registro. Solo gestiona identidades de usuarios registrados.\n"
            "- D: Customer 360 Identity NO se integra automáticamente con Data Manager y Audiences. Son productos separados que requieren configuración "
            "e integración explícita. La integración existe pero no es automática ni seamless como sugiere la opción."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.identity_overview.htm&type=5"
    },
    3: {
        "explanation": (
            "La respuesta correcta es B (Request Signing Certificate con certificado self-signed). "
            "La preocupación del responsable de IT es que el contenido del SAML AuthnRequest sea alterado durante el tránsito "
            "entre el SP (Salesforce) y el IdP. Esto es un problema de INTEGRIDAD, no de confidencialidad.\n\n"
            "En Salesforce, la página de configuración SSO tiene un campo llamado 'Request Signing Certificate'. Cuando se configura un certificado aquí, "
            "Salesforce firma digitalmente cada AuthnRequest SAML que envía al IdP. El IdP puede entonces verificar la firma usando la clave pública "
            "del certificado (que se comparte durante la configuración inicial), confirmando que el request no fue alterado en tránsito.\n\n"
            "Los certificados self-signed son perfectamente válidos para este propósito porque la confianza se establece fuera de banda (out-of-band) "
            "cuando el administrador comparte el certificado con el IdP durante la configuración. No se necesita una CA externa.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (HTTPS): Proporciona seguridad a nivel de transporte pero no protege contra manipulación del contenido SAML a nivel de aplicación.\n"
            "- C (Issuer y ACS URL): Son configuraciones básicas necesarias pero no previenen la alteración del request.\n"
            "- D (Encrypt): La encriptación protege la CONFIDENCIALIDAD (evita que se lea), no la INTEGRIDAD (evita que se altere). "
            "Además, Salesforce firma los requests, no los encripta. La firma digital es el mecanismo correcto para prevenir alteración."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.sso_saml_setting_up.htm&type=5"
    },
    4: {
        "explanation": (
            "Las respuestas correctas son A y D. Para implementar dynamic branding en un Experience Cloud site, se necesitan dos elementos clave.\n\n"
            "A es correcta: El Experience ID (expid) es un parámetro de URL que Salesforce usa para identificar qué marca/branding aplicar. "
            "Se incluye como parámetro en las URLs de OAuth, SAML y endpoints de la comunidad (ej: /services/oauth2/authorize?expid=valor). "
            "El placeholder parameter permite que la misma comunidad muestre diferentes apariencias según el parámetro recibido.\n\n"
            "D es correcta: Para usar dynamic branding, la comunidad debe construirse con el template 'Visualforce + Salesforce Tabs'. "
            "Este template permite mayor personalización programática del login page, incluyendo la capacidad de leer el parámetro expid "
            "y cambiar dinámicamente logos, colores y contenido. Los templates basados en Experience Builder (como Customer Account Portal) "
            "tienen un branding más estático configurado en el Builder.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- B (Customer Account Portal template): Este template usa Experience Builder para branding, que es más estático y no soporta "
            "dynamic branding basado en URL parameters de la misma forma.\n"
            "- C (CMS externo): No se requiere un CMS externo. Salesforce maneja el branding dinámico de forma nativa con expid."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.networks_login_page_branding.htm&type=5"
    },
    5: {
        "explanation": (
            "Las respuestas correctas son B, D y E. Para habilitar social sign-in en un sitio web B2C existente que no soporta SSO estándar, "
            "se necesitan tres componentes de Salesforce Identity trabajando juntos.\n\n"
            "B (Connected Apps): Las Connected Apps son necesarias para establecer la relación OAuth entre el sitio web externo y Salesforce. "
            "Definen los permisos, scopes y callbacks para la integración.\n\n"
            "D (Embedded Login): Embedded Login permite incrustar el formulario de inicio de sesión de Salesforce directamente en el sitio web B2C "
            "existente. Como el sitio no soporta SAML ni OAuth nativamente, Embedded Login proporciona un widget de login que se integra en la página "
            "sin requerir que el sitio implemente estos protocolos.\n\n"
            "E (Authentication Providers): Los Authentication Providers son la configuración en Salesforce que conecta con proveedores sociales "
            "(Google, Facebook, Twitter, etc.). Cada auth provider define la conexión OAuth/OIDC con el proveedor social.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (Identity Connect): Identity Connect es para sincronización con Microsoft Active Directory, no para social sign-in.\n"
            "- C (Delegated Authentication): Delegated Auth es para validar credenciales contra un sistema externo vía SOAP webservice, "
            "no tiene relación con social login. Además, está deprecado."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.embedded_login_for_web.htm&type=5"
    },
    6: {
        "explanation": (
            "Las respuestas correctas son B y C. En Salesforce Experience Cloud, cuando configuras un sitio y defines la experiencia de login, "
            "puedes elegir entre varios tipos de página de login en la sección Login & Registration de la administración del sitio.\n\n"
            "B (Experience Builder Page): Es una de las opciones principales. Permite crear una página de login personalizada usando Experience Builder, "
            "con componentes drag-and-drop, branding visual y layouts flexibles. Es la opción más moderna y recomendada.\n\n"
            "C (Login Discovery Page): Es otro tipo válido de página de login que permite implementar 'passwordless login' o login basado en "
            "identificador (email/teléfono). Login Discovery muestra un campo donde el usuario ingresa su identificador, y luego el sistema "
            "determina cómo autenticarlo (contraseña, verificación, SSO, etc.) usando un Login Discovery Handler (clase Apex).\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (Embedded Login Page): Embedded Login NO es un tipo de página de login para el sitio en sí. Es una funcionalidad para incrustar "
            "el login de Salesforce en páginas EXTERNAS (no-Salesforce). Es una solución para sitios web de terceros que quieren usar identidades de Salesforce.\n"
            "- D (Lightning Experience Page): Lightning Experience es la interfaz interna de Salesforce para usuarios internos. "
            "No es un tipo de página de login disponible para Experience Cloud sites."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.networks_customize_login_page.htm&type=5"
    },
    7: {
        "explanation": (
            "Las respuestas correctas son A y B. Al crear un Authentication Provider en Salesforce, la página de configuración ofrece "
            "varios campos configurables, entre los cuales destacan el Registration Handler y el Custom Error URL.\n\n"
            "A (Custom Registration Handler): Cuando se configura un Auth Provider, puedes asignar una clase Apex que implemente la interfaz "
            "Auth.RegistrationHandler. Esta clase se ejecuta cuando un usuario se autentica por primera vez a través del provider, "
            "permitiendo crear o vincular el usuario en Salesforce con lógica personalizada (asignar perfil, rol, cuenta, etc.).\n\n"
            "B (Custom Error URL): En la configuración del Auth Provider existe un campo 'Custom Error URL' que permite definir una URL "
            "a la que se redirige al usuario cuando ocurre un error durante la autenticación. Esto permite mostrar mensajes de error "
            "personalizados en lugar de la página de error genérica de Salesforce.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- C (Default login user): No existe un campo 'default login user' en la configuración del Auth Provider. "
            "Existe 'Execute Registration As' que es el usuario bajo cuyo contexto se ejecuta el registration handler, pero no es lo mismo.\n"
            "- D (Default authentication provider certificate): No existe este campo en la configuración del Auth Provider. "
            "Los certificados se configuran a nivel de Named Credentials o Connected Apps, no en Auth Providers."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.sso_provider_openid_connect.htm&type=5"
    },
    8: {
        "explanation": (
            "La respuesta correcta es A (Apex Just-in-Time handler para consultar atributos SAML custom y asignar permission sets). "
            "Este escenario requiere mapear grupos de Active Directory a Permission Sets en Salesforce de forma dinámica durante el login SSO.\n\n"
            "El Apex JIT Handler (clase que implementa Auth.SamlJitHandler) se ejecuta durante cada inicio de sesión SAML y tiene acceso completo "
            "a todos los atributos de la aserción SAML, incluyendo atributos personalizados (custom attributes). El IdP puede enviar los grupos "
            "de AD como atributos custom en la aserción SAML (ej: <Attribute Name='ADGroups'><AttributeValue>CRM_SuperUser</AttributeValue>...</Attribute>). "
            "El JIT handler puede leer estos atributos y programáticamente asignar o remover Permission Sets.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- B (Login flow + standard SAML attributes): Los Login Flows se ejecutan DESPUÉS de la autenticación y NO tienen acceso directo "
            "a los atributos SAML de la aserción. Además, los atributos standard de SAML no incluyen grupos de AD.\n"
            "- C (Login flow + custom SAML attributes): Mismo problema que B - los Login Flows no pueden acceder a atributos SAML.\n"
            "- D (JIT handler + standard SAML attributes): Los atributos SAML estándar (NameID, email, firstName, etc.) no incluyen "
            "información de grupos de AD. Se necesitan atributos CUSTOM para transmitir la membresía de grupos."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.sso_jit_implementation.htm&type=5"
    },
    9: {
        "explanation": (
            "La respuesta correcta es C (Salesforce Login History). "
            "Login History es la herramienta principal en Salesforce para auditar y verificar la actividad de autenticación de usuarios. "
            "Proporciona un registro detallado de cada intento de inicio de sesión.\n\n"
            "Login History registra información como: fecha/hora del intento, resultado (éxito/fallo), dirección IP de origen, "
            "tipo de login (UI, API, OAuth), navegador y plataforma del cliente, método de autenticación usado (password, SSO, MFA), "
            "geolocalización aproximada, y Application/Connected App utilizada. Esta información permite identificar patrones sospechosos "
            "como logins desde ubicaciones inusuales, múltiples fallos de autenticación, o accesos fuera de horario.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (Lightning Flow): Los Flows son herramientas de automatización de procesos, no de auditoría de login.\n"
            "- B (Approval Processes): Los procesos de aprobación gestionan flujos de aprobación de registros, no tienen relación con "
            "la auditoría de autenticación.\n"
            "- D (Salesforce Shield): Shield incluye Event Monitoring, Platform Encryption y Field Audit Trail. Aunque Event Monitoring "
            "puede rastrear actividad, es un producto adicional de pago. Login History es nativo y gratuito, y es la herramienta "
            "específica para el objetivo descrito en la pregunta."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.users_login_history.htm&type=5"
    },
    10: {
        "explanation": (
            "La respuesta correcta es C (Configurar Salesforce como Service Provider del IdP existente). "
            "NTO ya tiene un IdP de terceros que valida credenciales contra su directorio LDAP corporativo. El objetivo es que los empleados "
            "no necesiten recordar contraseñas adicionales para Salesforce.\n\n"
            "Al configurar Salesforce como SP (Service Provider) del IdP existente, los usuarios se autentican una sola vez en el IdP "
            "(usando sus credenciales LDAP) y obtienen acceso a Salesforce a través de SSO (Single Sign-On). No necesitan una contraseña "
            "separada para Salesforce porque la autenticación se delega completamente al IdP.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (Salesforce como IdP): No tiene sentido hacer Salesforce IdP cuando ya existe un IdP que maneja LDAP. "
            "Además, Salesforce no puede autenticar directamente contra un LDAP externo como IdP.\n"
            "- B (Salesforce Connect para sync passwords): Salesforce Connect es para acceso a datos externos (External Objects), "
            "no para sincronización de contraseñas. No existe esta funcionalidad.\n"
            "- D (Authentication Provider): Un Auth Provider en Salesforce se usa típicamente para autenticación social (OAuth/OIDC). "
            "Para SSO empresarial con un IdP existente, la configuración correcta es SAML SSO con Salesforce como SP. "
            "Un Auth Provider podría funcionar si el IdP soporta OIDC, pero la opción C es más precisa para el escenario descrito."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.sso_saml.htm&type=5"
    },
    11: {
        "explanation": (
            "La respuesta correcta es C (Authentication Provider + Registration Handler para cada proveedor social). "
            "Para habilitar login social con proveedores OpenID Connect, se necesitan dos componentes por cada proveedor.\n\n"
            "El Authentication Provider es la configuración en Salesforce que define la conexión con el proveedor social "
            "(Facebook, Google, etc.): consumer key, consumer secret, authorize endpoint, token endpoint, y scopes. "
            "Como todos los proveedores soportan OIDC, puedes usar el tipo 'OpenID Connect' genérico o los predefinidos.\n\n"
            "El Registration Handler es una clase Apex (implementa Auth.RegistrationHandler) que se ejecuta cuando un usuario "
            "se autentica exitosamente por primera vez. Su función es crear el registro de usuario en Salesforce, vincularlo "
            "a un Contact/Account, asignar perfil y licencia. Se necesita uno por cada provider porque la lógica puede variar.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (SSO setting + JIT handler): Las SSO settings son para SAML, no para OAuth/OIDC social login. JIT es para SAML.\n"
            "- B (Auth Provider + JIT handler): JIT provisioning es específico de SAML. Para Auth Providers (OAuth/OIDC), "
            "el mecanismo equivalente es el Registration Handler, no JIT.\n"
            "- D (SSO setting + Registration Handler): SSO settings son para SAML. Social sign-on usa Authentication Providers, no SSO settings."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.sso_authentication_providers.htm&type=5"
    },
    12: {
        "explanation": (
            "La respuesta correcta es A. Para renderizar la página de login dinámicamente según la preferencia de marca del usuario, "
            "se debe usar el parámetro expid (Experience ID) en la URL de autorización OAuth.\n\n"
            "El Experience ID (expid) es un mecanismo nativo de Salesforce que permite aplicar branding dinámico a una misma comunidad. "
            "Cuando la app en Heroku redirige al usuario para autorización OAuth, incluye el parámetro expid en la URL: "
            "community_url/services/oauth2/authorize/?expid=<valor>. Salesforce usa este valor para determinar qué conjunto de "
            "branding (logos, imágenes, colores) mostrar en la página de login.\n\n"
            "Esto permite que una sola comunidad sirva múltiples marcas sin duplicar infraestructura. El branding se configura "
            "en la administración de la comunidad asociando diferentes configuraciones visuales a diferentes valores de expid.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- B (Diferentes comunidades + Apex controller): Crear múltiples comunidades para cada marca es excesivo, costoso "
            "y difícil de mantener. expid resuelve esto con una sola comunidad.\n"
            "- C (cookie_value en URL): Esta sintaxis no existe en la API de OAuth de Salesforce. No hay un mecanismo de cookies "
            "en la URL de autorización para branding.\n"
            "- D (Experience Builder + Login Flows): Aunque Login Flows pueden personalizar la experiencia, no manejan branding "
            "dinámico basado en un parámetro externo de la misma forma que expid."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.networks_login_page_branding.htm&type=5"
    },
    13: {
        "explanation": (
            "La respuesta correcta es D (Establecer rangos de IP de confianza para la organización). "
            "Los prompts de verificación de identidad se activan cuando Salesforce detecta que un usuario está iniciando sesión "
            "desde una ubicación (IP) no reconocida o no confiable.\n\n"
            "Cuando configuras Trusted IP Ranges a nivel de organización (Setup > Network Access), Salesforce reconoce las conexiones "
            "desde esas IPs como confiables y NO dispara el desafío de verificación de identidad (Identity Verification). "
            "Esto reduce significativamente la frecuencia de prompts para usuarios que acceden desde ubicaciones corporativas conocidas.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (SSO con IdP externo): Implementar SSO cambia el método de autenticación, pero no necesariamente elimina los "
            "desafíos de verificación de identidad. Salesforce puede seguir verificando la identidad después del SSO si detecta riesgo.\n"
            "- B (MFA): Multi-Factor Authentication AUMENTA la seguridad pero no REDUCE los prompts de verificación. "
            "De hecho, habilitar MFA añade un paso adicional, no lo elimina.\n"
            "- C (2FA): Es prácticamente lo mismo que MFA. Añade un factor adicional, no reduce verificaciones.\n\n"
            "Es importante distinguir entre Identity Verification (desafío que Salesforce muestra ante actividad sospechosa) "
            "y MFA (requisito de seguridad adicional en cada login). Trusted IP Ranges afecta al primero."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.security_networkaccess.htm&type=5"
    },
    14: {
        "explanation": (
            "La respuesta correcta es B (Configurar Authentication Providers predefinidos para Facebook y Twitter). "
            "Salesforce proporciona Authentication Providers predefinidos (built-in) para los proveedores sociales más populares, "
            "incluyendo Facebook y Twitter.\n\n"
            "Los Auth Providers predefinidos simplifican enormemente la configuración porque Salesforce ya conoce los endpoints "
            "de autorización, token y user info de cada proveedor. Solo necesitas proporcionar el Consumer Key y Consumer Secret "
            "de tu aplicación registrada en Facebook/Twitter, y Salesforce maneja todo el flujo OAuth automáticamente.\n\n"
            "Salesforce incluye Auth Providers predefinidos para: Facebook, Google, Twitter/X, LinkedIn, Microsoft, Apple, "
            "y otros. Además del tipo genérico 'OpenID Connect' para cualquier proveedor compatible.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (Custom auth provider solo para Twitter): No es necesario crear un provider custom para Twitter. "
            "Salesforce ya tiene un provider predefinido para Twitter. Un custom provider solo se necesita para proveedores "
            "no soportados nativamente.\n"
            "- C (Custom auth provider solo para Facebook): Mismo razonamiento que A. Facebook tiene provider predefinido.\n"
            "- D (Login Flows): Los Login Flows se ejecutan DESPUÉS de la autenticación. No son el mecanismo para conectar "
            "con proveedores sociales. Los Auth Providers manejan la conexión OAuth; los Login Flows podrían añadir lógica post-login."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.sso_provider_facebook.htm&type=5"
    },
    15: {
        "explanation": (
            "Las respuestas correctas son A y C. Para implementar un CIAM mobile-first que soporte email o teléfono como username, "
            "se necesitan licencias External Identity y créditos de verificación SMS.\n\n"
            "C (External Identity Licenses): Las licencias External Identity son el tipo de licencia diseñado específicamente para "
            "usuarios externos en escenarios CIAM (Customer Identity and Access Management). Proporcionan acceso a Experience Cloud "
            "con funcionalidades de identidad (login, registro, perfil) sin acceso completo a CRM. Son más económicas que las "
            "licencias Community completas y están optimizadas para autenticación de usuarios externos.\n\n"
            "A (SMS Verification Credits): Cuando el requisito incluye usar el número de teléfono móvil como username y enviar "
            "códigos de verificación por SMS (para passwordless login o verificación de identidad), se necesitan SMS Verification Credits. "
            "Cada SMS enviado consume un crédito. Sin estos créditos, no se pueden enviar códigos por texto.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- B (Email Verification Credits): Los emails de verificación NO consumen créditos especiales en Salesforce. "
            "El envío de emails de verificación está incluido en las licencias estándar.\n"
            "- D (Identity Connect Licenses): Identity Connect es para sincronización con Active Directory (provisioning), "
            "no para autenticación de usuarios externos ni CIAM."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.users_license_types_communities.htm&type=5"
    },
    16: {
        "explanation": (
            "La respuesta correcta es C (Confirmar consideraciones de rendimiento con Salesforce Customer Support). "
            "Cuando un requisito involucra más de 1,000 logins por minuto en Salesforce Experience Cloud, "
            "esto excede los límites típicos de rendimiento y requiere coordinación con Salesforce.\n\n"
            "Salesforce tiene límites de tasa (rate limits) para autenticación que pueden afectar escenarios de alto volumen. "
            "La plataforma no está diseñada para manejar picos extremos de autenticación sin planificación previa. "
            "Antes de implementar una solución que requiera este volumen, es OBLIGATORIO contactar al equipo de soporte "
            "para: confirmar que la infraestructura puede manejar la carga, solicitar aumentos de límites si es necesario, "
            "y obtener recomendaciones de arquitectura para alto volumen.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (Community como SAML IdP + JIT): Aunque técnicamente posible, no aborda el problema principal de rendimiento "
            "a 1000 logins/min. Salesforce como IdP tiene límites que necesitan validación.\n"
            "- B (OAuth2 RPs con IdP externo): Esta es una arquitectura válida pero no garantiza que Salesforce pueda manejar "
            "el volumen. Aún necesitas confirmar con soporte.\n"
            "- D (Default account para ecommerce): PersonAccount SÍ es soportado en Experience Cloud. "
            "Esta opción contiene información incorrecta y no aborda el requisito de rendimiento."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.networks_limits.htm&type=5"
    },
    17: {
        "explanation": (
            "Las respuestas correctas son A y C. Para forzar a los usuarios a usar SOLO SSO (prohibiendo login con credenciales "
            "de Salesforce), se necesitan dos configuraciones complementarias.\n\n"
            "A ('Is Single Sign-On Enabled' permission): Este permiso a nivel de perfil o permission set habilita al usuario para "
            "utilizar SSO. Es un requisito previo para que el usuario pueda autenticarse a través del Identity Provider configurado. "
            "Sin este permiso, el usuario no podrá usar el flujo SSO.\n\n"
            "C (Enable My Domain + prevenir login desde login.salesforce.com): My Domain es un prerrequisito para SSO en Salesforce. "
            "Una vez habilitado, debes marcar la opción 'Prevent login from https://login.salesforce.com' en la configuración de "
            "My Domain. Esto bloquea el acceso al login page genérico de Salesforce, forzando a todos los usuarios a usar "
            "exclusivamente tu My Domain URL (donde está configurado el SSO).\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- B (Delegated Authentication): Delegated Authentication es un mecanismo de autenticación diferente (no SSO). "
            "Además, solicitarlo a Salesforce Support no es necesario para configurar SSO.\n"
            "- D (SSO auto-bloquea credenciales): FALSO. Habilitar SSO NO desactiva automáticamente el login con contraseña. "
            "Los usuarios pueden seguir usando username/password a menos que se tomen las medidas de A y C."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.sso_tips.htm&type=5"
    },
    18: {
        "explanation": (
            "La respuesta correcta es D (Identity Only License). "
            "Universal Containers necesita usar Salesforce Identity para controlar el acceso a una app externa para empleados. "
            "No necesitan acceso al CRM (Sales Cloud, Service Cloud), solo funcionalidad de identity provider.\n\n"
            "La licencia Identity Only es la licencia mínima requerida para usar Salesforce como Identity Provider. "
            "Permite a los usuarios: usar Single Sign-On desde Salesforce a aplicaciones externas, acceder al App Launcher, "
            "usar Connected Apps, y beneficiarse de las funcionalidades de identidad (MFA, session management, etc.) "
            "SIN acceso a objetos CRM como Leads, Opportunities, Cases, etc.\n\n"
            "Esta licencia es significativamente más económica que una licencia Salesforce completa y es ideal cuando "
            "los empleados solo necesitan Salesforce como hub de identidad para acceder a otras aplicaciones.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (Identity Connect): Identity Connect es un PRODUCTO (software on-premise para sincronizar Active Directory), "
            "no un tipo de licencia de usuario.\n"
            "- B (External Identity): Esta licencia es para usuarios EXTERNOS (clientes, partners en Experience Cloud), "
            "no para empleados internos.\n"
            "- C (Identity Verification): No existe una licencia llamada 'Identity Verification'. "
            "Identity Verification Credits son créditos para SMS, no una licencia de usuario."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.users_license_types_available.htm&type=5"
    },
    19: {
        "explanation": (
            "Las respuestas correctas son B y C. Para la app móvil usando user-agent flow donde los usuarios no deben "
            "aprobar acceso API ni re-autenticarse durante 3 meses, se necesitan dos configuraciones en la Connected App.\n\n"
            "B (Permitted Users = 'Admin approved users are pre-authorized'): Esta configuración elimina la pantalla de "
            "consentimiento OAuth. Normalmente, la primera vez que un usuario accede a una Connected App, ve una pantalla "
            "pidiendo que autorice el acceso. Con 'Admin approved users are pre-authorized', los usuarios asignados (vía perfil "
            "o permission set) están pre-autorizados y NUNCA ven la pantalla de consentimiento.\n\n"
            "C (Refresh Token Policy = expire after 3 months): El Refresh Token permite obtener nuevos Access Tokens sin "
            "que el usuario se re-autentique. Configurando la política de refresh token para expirar a los 3 meses, "
            "la app puede renovar tokens silenciosamente durante ese período. Después de 3 meses, el usuario deberá "
            "re-autenticarse.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (Session Timeout = 3 months): El session timeout controla cuánto dura una sesión individual, no el período "
            "total sin re-autenticación. Además, sesiones de 3 meses no son práctica estándar.\n"
            "- D (All users may self-authorize): Esta opción MUESTRA la pantalla de consentimiento, que es exactamente lo "
            "que el requisito dice evitar ('not be forced to approve API access')."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.connected_app_manage_oauth.htm&type=5"
    },
    20: {
        "explanation": (
            "Las respuestas correctas son C y D. Los errores 'Replay Detected' y 'Assertion Invalid' son errores SAML específicos "
            "con causas bien definidas.\n\n"
            "C (Assertion ID previamente usado - causa 'Replay Detected'): Salesforce mantiene un registro de los IDs de aserciones "
            "SAML procesadas. Si recibe una aserción con un ID que ya fue usado anteriormente (posible ataque de replay o "
            "el IdP reutilizando IDs), Salesforce rechaza la aserción con error 'Replay Detected'. Cada aserción SAML debe "
            "tener un ID único e irrepetible.\n\n"
            "D (Tiempo desincronizado >8 minutos - causa 'Assertion Invalid'): Las aserciones SAML incluyen condiciones "
            "temporales (NotBefore y NotOnOrAfter). Salesforce permite una tolerancia de hasta 3-5 minutos de diferencia "
            "entre relojes. Si la diferencia entre el reloj del IdP y Salesforce supera este umbral (la pregunta dice 8 min), "
            "la aserción se considera inválida porque parece estar expirada o ser del futuro.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (Certificado no coincide): Un certificado incorrecto causa 'Signature Validation Error', no 'Replay Detected' "
            "ni 'Assertion Invalid'.\n"
            "- B (Subject element faltante): Un subject faltante causaría un error de formato/estructura, "
            "no específicamente los errores mencionados en la pregunta."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.sso_saml_validation_errors.htm&type=5"
    },
    21: {
        "explanation": (
            "La respuesta correcta es C (Crear custom scopes y asignarlos a la Connected App). "
            "Los Custom OAuth Scopes permiten definir permisos granulares y flexibles para controlar exactamente qué datos "
            "y operaciones puede acceder una aplicación externa.\n\n"
            "En Salesforce, además de los scopes estándar (api, web, refresh_token, openid, etc.), puedes crear Custom Scopes "
            "que definen acceso a recursos específicos. Estos scopes personalizados se crean y se asignan a Connected Apps, "
            "permitiendo un control granular sobre qué datos del recurso protegido son accesibles. "
            "Esto es 'flexible' porque puedes crear tantos scopes como necesites y combinarlos según los requisitos de cada app.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (Admin approved + profiles): Esto controla QUIÉN puede acceder a la app, no QUÉ DATOS pueden acceder. "
            "La pregunta pide limitar 'the level of access to the data', no quién tiene acceso.\n"
            "- B (Permission set): Los permission sets controlan permisos dentro de Salesforce para el usuario, "
            "no limitan específicamente lo que una app OAuth puede hacer. No ofrecen la flexibilidad que pide la pregunta "
            "para el acceso de la aplicación externa.\n"
            "- D (External objects + data classification): Los external objects son para acceder a datos FUERA de Salesforce. "
            "Data classification policies son para clasificar datos, no para controlar acceso OAuth."
        ),
        "reference": "https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/intro_oauth_and_connected_apps.htm"
    },
    22: {
        "explanation": (
            "La respuesta correcta es A. Los pasos para habilitar JIT provisioning una vez que SAML SSO ya está configurado son: "
            "1) Habilitar JIT en la configuración SAML, 2) Elegir el tipo de provisioning, y 3) Proporcionar el handler.\n\n"
            "En la página de Single Sign-On Settings de Salesforce, después de configurar los parámetros SAML básicos, "
            "debes marcar el checkbox 'User Provisioning Enabled' (Just-in-Time User Provisioning). Luego seleccionas el "
            "tipo de provisioning: 'Standard' (mapeo declarativo de atributos SAML a campos de usuario) o 'Custom SAML JIT with Apex' "
            "(usa una clase Apex que implementa Auth.SamlJitHandler para lógica personalizada). Si eliges Custom, "
            "debes especificar la clase Apex del SAML JIT Handler.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- B (Permission set con JIT): No existe un permission set que habilite JIT. JIT se configura en la "
            "SAML SSO Setting, no a través de permisos de usuario.\n"
            "- C (Organization-wide sharing + sharing rules): Las reglas de compartición controlan visibilidad de registros "
            "entre usuarios. No tienen ninguna relación con el aprovisionamiento JIT.\n"
            "- D (Crear clase Apex + asignar a profiles): Aunque la parte de Apex podría ser correcta para JIT Custom, "
            "la clase se asigna en la SSO Setting (no en profiles), y primero debes habilitar JIT en la configuración SAML. "
            "La opción D omite el paso crucial de habilitar JIT en la SSO Setting."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.sso_jit_about.htm&type=5"
    },
    23: {
        "explanation": (
            "La respuesta correcta es C (Configure User Provisioning for Connected App). "
            "Salesforce ofrece una funcionalidad nativa de User Provisioning para Connected Apps que permite automatizar "
            "la gestión del ciclo de vida de usuarios en aplicaciones externas conectadas.\n\n"
            "La funcionalidad 'User Provisioning for Connected Apps' utiliza el estándar SCIM (System for Cross-domain Identity Management) "
            "o conectores personalizados para sincronizar operaciones de usuario entre Salesforce y la app externa. "
            "Cuando se habilita, permite: crear usuarios en la app externa cuando se crean en Salesforce, "
            "desactivar/suspender usuarios cuando se congelan en Salesforce, reactivar usuarios, y actualizar atributos. "
            "Todo esto de forma automatizada y bidireccional.\n\n"
            "Para Google Workspace específicamente, Salesforce proporciona un conector pre-construido que permite "
            "configurar este provisioning sin código.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (Apex trigger en UserLogin + callouts): Crear triggers custom es desarrollo innecesario cuando existe "
            "la funcionalidad nativa. Además, triggers con callouts asíncronos son frágiles y difíciles de mantener.\n"
            "- B (REST endpoint + polling): Polling es ineficiente y tiene latencia. El provisioning nativo es event-driven.\n"
            "- D (SAML JIT handler): JIT provisioning es para crear usuarios EN Salesforce durante login SSO. "
            "La pregunta pide lo contrario: provisionar usuarios DESDE Salesforce hacia Google Workspace."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.connected_app_user_provisioning.htm&type=5"
    },
    24: {
        "explanation": (
            "La respuesta correcta es B (Activations feature). "
            "La funcionalidad de Activations en Salesforce permite rastrear información sobre los dispositivos desde los que "
            "los usuarios inician sesión y proporciona la capacidad de revocar el acceso de dispositivos específicos.\n\n"
            "Activations registra: tipo de dispositivo, navegador, sistema operativo, fecha de primera y última activación, "
            "y ubicación. Los administradores de seguridad pueden ver todos los dispositivos activos de un usuario y "
            "revocar (desactivar) cualquier dispositivo específico. Cuando se revoca, el usuario deberá verificar su identidad "
            "nuevamente desde ese dispositivo.\n\n"
            "Esta funcionalidad está accesible en Setup > Identity Verification History y en el registro de cada usuario "
            "bajo la sección 'Activations'. Cumple exactamente con los dos requisitos: tracking + capacidad de revocación.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (Login History): Login History registra los intentos de login con información del dispositivo, PERO "
            "no permite REVOCAR dispositivos. Solo es para consulta/auditoría, no para acción.\n"
            "- C (Login Flows + custom object): Esto requeriría desarrollo personalizado extenso y no proporcionaría "
            "la funcionalidad de revocación de forma nativa. Activations lo hace out-of-the-box.\n"
            "- D (MFA): Multi-Factor Authentication añade seguridad pero no es una herramienta de tracking de dispositivos "
            "ni permite revocar dispositivos específicos."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.security_activation_about.htm&type=5"
    },
    25: {
        "explanation": (
            "La respuesta correcta es A (User Management). "
            "En este escenario, NTO ya tiene un SSO solution de terceros que maneja la autenticación. "
            "Identity Connect se está evaluando específicamente para 'automatic provisioning and deprovisioning'. "
            "Esto es User Management, no SSO.\n\n"
            "Identity Connect es un software on-premise que actúa como puente entre Microsoft Active Directory y Salesforce. "
            "Sus funciones principales son: sincronización de usuarios (crear en SF cuando se crea en AD), "
            "actualización de atributos (sync de campos), desactivación de usuarios (deprovisioning cuando se deshabilita en AD), "
            "y sincronización de contraseñas. Todas estas son funciones de USER MANAGEMENT.\n\n"
            "En este caso específico, el rol de Identity Connect es exclusivamente User Management porque:\n"
            "1. El SSO ya lo maneja otra solución de terceros\n"
            "2. NTO solo quiere provisioning/deprovisioning automático\n"
            "3. Identity Connect sincronizará usuarios AD↔Salesforce sin manejar la autenticación\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- B (SSO): Aunque Identity Connect CAN proporcionar SSO, en este escenario ya tienen SSO cubierto por otro producto.\n"
            "- C (Identity Provider): Identity Connect NO es un Identity Provider. No autentica usuarios.\n"
            "- D (Service Provider): Identity Connect NO es un Service Provider. Es un middleware de sincronización."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.identity_connect_basics.htm&type=5"
    },
    26: {
        "explanation": (
            "La respuesta correcta es A (Implementar una solución de identidad federada basada en SAML). "
            "SAML (Security Assertion Markup Language) es el estándar de la industria para establecer confianza federada "
            "entre sistemas de identidad, permitiendo autenticación cross-domain sin compartir credenciales.\n\n"
            "La identidad federada con SAML permite que un usuario se autentique en un sistema (el IdP/directorio externo) "
            "y ese sistema emita una aserción firmada digitalmente que Salesforce (como SP) acepta para otorgar acceso. "
            "Se establece confianza mediante intercambio de certificados y metadatos entre ambos sistemas.\n\n"
            "SAML es específicamente diseñado para este caso de uso: integrar un directorio central (repositorio de autenticación "
            "y autorización) con múltiples sistemas, incluyendo Salesforce. Es el mecanismo estándar de confianza entre "
            "organizaciones y sistemas heterogéneos.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- B (IP-based restrictions): Las restricciones de IP controlan DESDE DÓNDE se puede acceder, pero no establecen "
            "confianza entre sistemas ni permiten autenticación federada.\n"
            "- C (Email-based verification): La verificación por email es un método de verificación de identidad básico, "
            "no un protocolo de federación de identidades entre sistemas.\n"
            "- D (Shared database table): Compartir credenciales en una tabla de base de datos es inseguro, no escalable, "
            "y viola principios fundamentales de seguridad (contraseñas no deben compartirse entre sistemas)."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.sso_saml.htm&type=5"
    },
    27: {
        "explanation": (
            "La respuesta correcta es B (Usar Login Flows para mostrar alertas personalizadas). "
            "Los Login Flows son flujos que se ejecutan después de la autenticación pero ANTES de que el usuario llegue a la página "
            "principal. Son perfectos para mostrar pantallas intermedias con información personalizada.\n\n"
            "Un Login Flow puede incluir screens (pantallas) que muestren mensajes personalizados basados en el perfil del usuario, "
            "sus datos, o cualquier lógica de negocio. Se configuran declarativamente usando Flow Builder y se asignan al sitio "
            "en la configuración de Login & Registration. Esto cumple el requisito con 'least amount of customization' porque:\n"
            "1. No requiere código (es declarativo, usando Flow Builder)\n"
            "2. Se ejecuta en el momento exacto correcto (post-login, pre-homepage)\n"
            "3. Puede personalizar mensajes por usuario usando variables de Flow\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (LWC en homepage): Un componente en la homepage se mostraría DESPUÉS de que el usuario ya llegó a la home. "
            "El requisito dice 'before they land on the homepage'.\n"
            "- C (Registration handler + routing): El registration handler solo se ejecuta durante el registro/primer login, "
            "no en cada login. Además, requiere código Apex (más customization).\n"
            "- D (Custom metadata + LWC): Requiere desarrollo de código (LWC + Apex para leer metadata). "
            "No es la opción con 'least amount of customization'."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.security_login_flow.htm&type=5"
    },
    28: {
        "explanation": (
            "Las respuestas correctas son A y C. Para que una Connected App aparezca como tile en el App Launcher, "
            "se necesitan dos configuraciones específicas.\n\n"
            "A ('Visible in App Launcher' no está habilitado): En la configuración de la Connected App, bajo la sección "
            "'App Menu', existe una opción para hacer visible la app en el App Launcher. Si no está marcada, el tile no aparece "
            "independientemente de otras configuraciones.\n\n"
            "C (StartURL no configurada): El StartURL es la URL a la que se redirige al usuario cuando hace clic en el tile "
            "del App Launcher. Sin un StartURL configurado, Salesforce no puede crear un tile funcional porque no sabe "
            "a dónde dirigir al usuario. Es un campo requerido para que el tile aparezca.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- B (OAuth scope sin 'openid'): Los OAuth scopes definen qué datos puede acceder la app. No afectan la "
            "visibilidad en el App Launcher. Una app puede ser visible sin el scope 'openid'.\n"
            "- D (High Assurance Session required): Esta política de sesión puede requerir verificación adicional al ACCEDER "
            "a la app, pero no impide que el TILE sea visible. El tile aparece; simplemente se requiere step-up auth al clickear."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.connected_app_manage.htm&type=5"
    },
    29: {
        "explanation": (
            "La respuesta correcta es D (Session Settings). "
            "Para aplicar restricciones de IP y timeout de sesión de forma centralizada que afecten a las Connected Apps, "
            "se configuran en Session Settings de la organización.\n\n"
            "En Setup > Session Settings, el administrador puede configurar: timeout de sesión (desde 15 minutos hasta 24 horas), "
            "restricciones de IP para sesiones, requisitos de seguridad para sesiones, y otras políticas de sesión que aplican "
            "globalmente. Estas configuraciones afectan a todas las sesiones, incluyendo las iniciadas a través de Connected Apps.\n\n"
            "Las Session Settings proporcionan un punto central de configuración para políticas de sesión que cubren tanto "
            "las restricciones de IP (lock sessions to the IP address from which they originated) como los timeouts "
            "(session timeout value). Esto aplica de forma uniforme a las sesiones creadas por Connected Apps.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (Login IP Ranges): Estas se configuran a nivel de PERFIL y controlan desde dónde puede iniciar sesión un usuario, "
            "pero no específicamente timeout de sesión ni políticas para la Connected App.\n"
            "- B (Custom Permissions): Las Custom Permissions controlan acceso a funcionalidades específicas en código Apex/Flows, "
            "no tienen relación con IP o session timeout.\n"
            "- C (Connected App OAuth policies): Las OAuth policies de la Connected App incluyen IP Relaxation y Refresh Token Policy, "
            "pero la pregunta pregunta por una solución que cubra AMBOS (IP restrictions Y session timeout) de forma integrada."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.admin_sessions.htm&type=5"
    },
    30: {
        "explanation": (
            "La respuesta correcta es C (Salesforce será el Service Provider). "
            "Cuando una organización permite que sus usuarios inicien sesión con credenciales de Facebook o LinkedIn, "
            "esos proveedores sociales actúan como Identity Providers y Salesforce actúa como Service Provider.\n\n"
            "En el contexto de identidad federada:\n"
            "- Identity Provider (IdP): El sistema que AUTENTICA al usuario y valida sus credenciales. En este caso, "
            "Facebook y LinkedIn verifican la identidad del usuario.\n"
            "- Service Provider (SP): El sistema que RECIBE la confirmación de autenticación y otorga acceso. "
            "Salesforce recibe la confirmación de que el usuario se autenticó exitosamente en Facebook/LinkedIn "
            "y le permite acceder al Experience Cloud.\n\n"
            "Salesforce como SP utiliza Authentication Providers configurados con las credenciales OAuth de Facebook/LinkedIn "
            "para completar el flujo de autenticación social.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (Facebook/LinkedIn como SPs): Es al revés. Los proveedores sociales son IdPs, no SPs. "
            "Son ellos quienes autentican al usuario.\n"
            "- B (Facebook/LinkedIn como IdPs Y SPs): Solo actúan como IdPs en este flujo. No son SPs de nada aquí.\n"
            "- D (Salesforce como IdP): Salesforce NO está autenticando al usuario en este escenario. "
            "Está delegando la autenticación a Facebook/LinkedIn, por lo tanto es SP, no IdP."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.sso_authentication_providers.htm&type=5"
    },
    31: {
        "explanation": (
            "La respuesta correcta es D (Delegated Authentication). "
            "Cuando el requisito es que las credenciales y la autenticación sean gestionadas por un sistema externo "
            "accesible SOLO vía SOAP webservice, Delegated Authentication es la solución correcta.\n\n"
            "Delegated Authentication funciona así: cuando un usuario intenta iniciar sesión en Salesforce con username/password, "
            "en lugar de validar la contraseña internamente, Salesforce envía las credenciales a un endpoint SOAP externo "
            "(el webservice del sistema de autenticación corporativo). El sistema externo valida contra su LDAP/directorio "
            "y responde con true/false. Si es true, Salesforce concede acceso.\n\n"
            "Esto cumple exactamente los requisitos regulatorios: el sistema externo mantiene control total sobre "
            "la gestión de contraseñas y solicitudes de autenticación, mientras que Salesforce delega esta responsabilidad.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (OAuth Web-Server Flow): OAuth es para autorización de acceso a APIs, no para autenticación de login de usuarios. "
            "No permite que un sistema externo valide credenciales durante el login a Salesforce.\n"
            "- B (JIT Provisioning): JIT crea/actualiza usuarios durante login SSO. No maneja autenticación ni "
            "validación de contraseñas.\n"
            "- C (SAML SSO): SAML requiere que el IdP soporte SAML protocol. La pregunta especifica que el sistema externo "
            "SOLO es accesible vía SOAP webservice. SAML usa HTTP redirects/POSTs, no SOAP. "
            "Delegated Auth usa SOAP, que es exactamente lo que soporta el sistema externo."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.sso_delauthentication.htm&type=5"
    },
    32: {
        "explanation": (
            "Las respuestas correctas son B, C y D (Client ID, Scopes, Refresh Token). "
            "Estos tres conceptos OAuth aplican al flujo user-agent de Salesforce.\n\n"
            "B (Client ID): En el user-agent flow, la aplicación móvil incluye el client_id (Consumer Key de la Connected App) "
            "en la solicitud de autorización. Es obligatorio para identificar qué aplicación está solicitando acceso.\n\n"
            "C (Scopes): Los scopes se envían en la solicitud de autorización para definir qué nivel de acceso necesita la app "
            "(api, web, refresh_token, openid, etc.). Son fundamentales para limitar los permisos.\n\n"
            "D (Refresh Token): Aunque el OAuth 2.0 implicit grant estándar (RFC 6749) NO incluye refresh tokens, "
            "la implementación de Salesforce del user-agent flow SÍ puede devolver un refresh token si la Connected App "
            "tiene configurada una Refresh Token Policy. Esto permite a la app móvil obtener nuevos access tokens sin "
            "que el usuario se re-autentique.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (Verification Code): No existe un 'Verification Code' como concepto OAuth en este flujo. "
            "Los device codes son del Device Flow, no del user-agent flow.\n"
            "- E (Authorization Code): El Authorization Code es del WEB SERVER flow (authorization code grant). "
            "El user-agent flow (implicit grant) devuelve el token DIRECTAMENTE en el fragment de la URL, "
            "sin un código intermedio."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.remoteaccess_oauth_user_agent_flow.htm&type=5"
    },
    33: {
        "explanation": (
            "La respuesta correcta es C (OAuth Device Flow). "
            "El escenario describe un fitness tracker (dispositivo con capacidades de entrada limitadas) que necesita "
            "conectarse al perfil del usuario en la comunidad de Salesforce.\n\n"
            "El OAuth 2.0 Device Flow está diseñado específicamente para dispositivos que tienen capacidades de entrada "
            "limitadas (sin teclado completo, sin navegador full) como fitness trackers, smart TVs, o dispositivos IoT. "
            "El flujo funciona así:\n"
            "1. El dispositivo solicita un device code y un user code\n"
            "2. El usuario va a una URL de verificación en su teléfono/computadora\n"
            "3. El usuario ingresa el user code para autorizar el dispositivo\n"
            "4. El dispositivo recibe un access token y puede acceder a Salesforce\n\n"
            "Esto permite al fitness tracker conectarse al perfil del cliente sin que el usuario necesite "
            "escribir credenciales en el dispositivo.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (Login Flows): Los Login Flows son flujos post-autenticación en Salesforce, no mecanismos de "
            "autorización para dispositivos externos.\n"
            "- B (OAuth Asset Token Flow): Asset Token es para dispositivos IoT que ya están registrados y necesitan "
            "tokens derivados para operar autónomamente. No es para la conexión/registro inicial del dispositivo.\n"
            "- D (Named Credentials): Named Credentials almacenan credenciales para callouts SALIENTES desde Salesforce, "
            "no para autenticación de dispositivos ENTRANTES."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.remoteaccess_oauth_device_flow.htm&type=5"
    },
    34: {
        "explanation": (
            "La respuesta correcta es B (JWT Bearer Flow). "
            "El JWT Bearer Token Flow es ideal para integraciones server-to-server donde se necesita minimizar "
            "la interacción del usuario y maximizar la seguridad.\n\n"
            "El JWT Bearer Flow funciona así: el sistema externo crea un JWT (JSON Web Token) firmado con su clave privada, "
            "incluyendo claims sobre la identidad y los permisos solicitados. Lo envía al token endpoint de Salesforce. "
            "Salesforce valida la firma usando el certificado público registrado en la Connected App, y si es válido, "
            "devuelve un access token. TODO ESTO SIN INTERACCIÓN DEL USUARIO.\n\n"
            "Maximiza seguridad porque: usa certificados digitales (no client_secret), no transmite credenciales de usuario, "
            "los tokens tienen vida corta, y el JWT está firmado criptográficamente. "
            "Minimiza interacción del usuario porque no requiere login ni consentimiento.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (Username-Password Flow): Transmite username y password en texto (aunque por HTTPS). "
            "Requiere almacenar credenciales en el sistema externo. Menos seguro que JWT.\n"
            "- C (Web Server Flow): Requiere interacción del usuario (login + consentimiento en navegador). "
            "No es adecuado para server-to-server sin UI.\n"
            "- D (User Agent Flow): También requiere interacción del usuario y un navegador. "
            "Es para apps client-side (móviles/SPA), no para server-to-server."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.remoteaccess_oauth_jwt_flow.htm&type=5"
    },
    35: {
        "explanation": (
            "La respuesta correcta es A (Descargar Login History y evaluar los detalles de logins del usuario). "
            "Como primer paso en un análisis forense de una cuenta posiblemente comprometida, "
            "Login History proporciona las señales más inmediatas y relevantes.\n\n"
            "Login History contiene información crítica para detectar compromiso: IPs de origen (¿hay IPs desconocidas?), "
            "geolocalización (¿logins desde países inesperados?), horarios (¿actividad fuera de horario laboral?), "
            "tipo de login (¿se usó API de forma inusual?), navegador/dispositivo (¿dispositivos no reconocidos?), "
            "estado de la autenticación (¿fallos seguidos de un éxito? = posible brute force), y método de autenticación.\n\n"
            "Estas son exactamente las 'signals that could indicate a breach' que se piden en la pregunta.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- B (Identity Provider Event Log): Este log registra actividad de Salesforce COMO IdP (cuando otros apps "
            "se autentican VÍA Salesforce). No es el primer paso para analizar compromiso de la cuenta misma.\n"
            "- C (Setup Audit Trail): Registra cambios de CONFIGURACIÓN (campos creados, perfiles modificados, etc.), "
            "no actividad de login. Es útil pero no es el PRIMER paso para señales de compromiso de cuenta.\n"
            "- D (User record): El registro de usuario muestra el último login y configuración, "
            "pero no proporciona el historial detallado necesario para análisis forense."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.users_login_history.htm&type=5"
    },
    36: {
        "explanation": (
            "Las respuestas correctas son A, D y E (Scopes, Client Secret, Access Token). "
            "Estos tres conceptos son fundamentales en el OAuth 2.0 Web Server Flow (Authorization Code Grant).\n\n"
            "A (Scopes): En la solicitud de autorización, la app especifica los scopes que necesita "
            "(api, web, refresh_token, etc.). Definen qué permisos se solicitan.\n\n"
            "D (Client Secret): El Client Secret (Consumer Secret) se usa en el paso de intercambio del Authorization Code "
            "por el Access Token. La app envía client_id + client_secret + authorization_code al token endpoint. "
            "El Client Secret es EXCLUSIVO del Web Server Flow porque se transmite server-to-server de forma segura. "
            "El user-agent flow NO usa Client Secret porque la app client-side no puede guardarlo de forma segura.\n\n"
            "E (Access Token): El resultado final del flujo es un Access Token que la app usa para hacer API calls a Salesforce.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- B (Verification URL): No existe un concepto de 'Verification URL' en el Web Server Flow. "
            "Las Verification URLs son del Device Flow.\n"
            "- C (Authentication Token): No existe un 'Authentication Token' como concepto OAuth estándar. "
            "Los tokens OAuth son Access Token y Refresh Token, no 'Authentication Token'."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.remoteaccess_oauth_web_server_flow.htm&type=5"
    },
    37: {
        "explanation": (
            "La respuesta correcta es D (OAuth 2.0 Device Flow). "
            "El OAuth 2.0 Device Authorization Flow está diseñado específicamente para dispositivos IoT "
            "con capacidades limitadas de display o input (sin teclado, sin navegador web completo).\n\n"
            "Un dispositivo IoT con pantalla limitada no puede mostrar una página web de login ni permitir que "
            "el usuario escriba credenciales. El Device Flow resuelve esto permitiendo que el dispositivo muestre "
            "un código simple (user code) y una URL corta. El usuario va a esa URL en su teléfono/computadora, "
            "ingresa el código, y autoriza el dispositivo. El dispositivo luego recibe el access token.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (User-Agent Flow): Requiere un navegador web completo en el dispositivo para mostrar la página "
            "de autorización de Salesforce. Un dispositivo IoT con display limitado no puede hacer esto.\n"
            "- B (Asset Token Flow): Asset Token es para dispositivos que ya están registrados y autorizados "
            "y necesitan tokens derivados para sub-dispositivos. No es para el registro/autorización inicial.\n"
            "- C (JWT Bearer Flow): Requiere un certificado pre-configurado y es para autenticación server-to-server "
            "sin intervención del usuario. Para IoT con registro de usuario, Device Flow es más apropiado "
            "porque requiere la autorización explícita del usuario propietario del dispositivo."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.remoteaccess_oauth_device_flow.htm&type=5"
    },
    38: {
        "explanation": (
            "La respuesta correcta es B (Login History). "
            "Cuando los usuarios reciben errores al iniciar sesión vía SSO con un IdP externo, "
            "Login History es la primera herramienta para diagnosticar el problema.\n\n"
            "Login History en Salesforce registra cada intento de autenticación, incluyendo los fallidos. "
            "Para errores de SSO/SAML, muestra información como: el error específico (Assertion Expired, "
            "Invalid Signature, Recipient Mismatch, etc.), la hora del intento, el IdP que envió la aserción, "
            "y otros detalles que ayudan a identificar la causa raíz.\n\n"
            "En el contexto de una universidad con IdP externo donde los usuarios tienen errores al hacer login, "
            "Login History mostrará exactamente qué tipo de error SAML está ocurriendo, lo cual es el punto de partida "
            "para cualquier debugging de SSO.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (Setup Audit Trail): Registra cambios de configuración administrativa, no errores de login. "
            "Útil para ver si alguien modificó la configuración SSO, pero no para ver errores de autenticación.\n"
            "- C (Apex Exception Email): Solo aplica si hay código Apex ejecutándose (JIT handlers, registration handlers). "
            "Si el SSO básico falla antes de ejecutar Apex, no generará exception emails.\n"
            "- D (Debug Logs): Los Debug Logs registran ejecución de código Apex. El proceso SAML SSO no genera "
            "debug logs útiles a menos que haya un JIT handler involucrado."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.users_login_history.htm&type=5"
    },
    39: {
        "explanation": (
            "Las respuestas correctas son B y D. Para un Canvas App que usa Enterprise SSO (SAML) donde los agentes "
            "no deben necesitar login adicional, se necesitan estas dos configuraciones.\n\n"
            "B (Connected App como admin-approved pre-authorized): Configurar la Canvas app como Connected App con "
            "'Admin approved users are pre-authorized' elimina cualquier pantalla de consentimiento OAuth. "
            "Los usuarios asignados (vía perfil o permission set) están pre-autorizados, por lo que el acceso "
            "es seamless sin prompts adicionales.\n\n"
            "D (Enable SAML + SP Initiated): Al habilitar SAML en la Connected App y configurar el SAML Initiation Method "
            "como 'Service Provider Initiated', la pricing application (Canvas app) puede iniciar el proceso de SSO. "
            "Cuando el agente accede al Canvas app, ésta inicia el flujo SAML SP-initiated, y como el Enterprise SSO "
            "ya tiene una sesión activa, el agente se autentica transparentemente.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (Enable as Canvas Personal App): Canvas Personal Apps son aplicaciones que los usuarios instalan "
            "individualmente en su Chatter feed. No es relevante para una app empresarial de pricing para el call center.\n"
            "- C (OAuth settings con scopes): Aunque OAuth puede ser usado para Canvas, la pregunta específica Enterprise SSO "
            "(SAML-based) y la opción D aborda directamente cómo integrar la Canvas app con SAML SSO existente."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.connected_app_create_canvas.htm&type=5"
    },
    40: {
        "explanation": (
            "La respuesta correcta es B (Login Discovery Page con Login Discovery Handler). "
            "Login Discovery es la funcionalidad de Salesforce diseñada para permitir que los usuarios "
            "inicien sesión usando un identificador (teléfono o email) en lugar de un username tradicional, "
            "y luego verificar su identidad con un código.\n\n"
            "El Login Discovery Page presenta al usuario un campo donde ingresa su identificador (teléfono o email). "
            "El Login Discovery Handler (clase Apex que implementa MyDomainLoginDiscoveryHandler) contiene la lógica para: "
            "1) Buscar al usuario por teléfono o email, 2) Determinar el método de verificación (SMS o email), "
            "3) Enviar el código de verificación, 4) Verificar el código ingresado por el usuario.\n\n"
            "Este es exactamente el flujo descrito en los requisitos: ingresa teléfono/email → recibe código → verifica.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (Custom login flow + Apex controller): Los Login Flows se ejecutan DESPUÉS de la autenticación, "
            "no COMO la autenticación. No pueden reemplazar el login page principal.\n"
            "- C (Custom login page + Apex): Requiere desarrollo extenso y no usa la funcionalidad nativa "
            "de Login Discovery que Salesforce proporciona para este caso exacto.\n"
            "- D (Auth Provider + self-registration): Los Auth Providers son para autenticación con IdPs externos. "
            "Self-registration es para crear nuevas cuentas, no para login de usuarios existentes."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.security_login_discovery.htm&type=5"
    },
    41: {
        "explanation": (
            "La respuesta correcta es B (OAuth 2.0 Asset Token Flow). "
            "El Asset Token Flow está diseñado para escenarios IoT donde dispositivos conectados (assets) "
            "necesitan comunicarse con Salesforce de forma autónoma para enviar datos o alertas.\n\n"
            "En este escenario, los sensores agrícolas (livestock tracking, pest monitoring, climate monitoring) "
            "son 'assets' registrados que necesitan enviar alertas a Salesforce cuando detectan problemas. "
            "El Asset Token Flow permite que estos dispositivos obtengan tokens de acceso para comunicarse con "
            "Salesforce sin intervención del usuario, ideal para dispositivos que operan de forma autónoma 24/7.\n\n"
            "El flujo funciona: el dispositivo recibe un actor token durante el registro inicial. Luego puede "
            "intercambiar este actor token por access tokens para hacer API calls a Salesforce "
            "(como crear un Case cuando el sensor detecta un problema).\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (SAML Bearer Assertion): SAML Bearer es para integración entre sistemas que usan SAML. "
            "No es apropiado para dispositivos IoT que necesitan comunicación directa con APIs.\n"
            "- C (Device Authentication Flow): El Device Flow es para que un USUARIO autorice un dispositivo "
            "interactivamente. Los sensores agrícolas operan autónomamente sin intervención humana continua.\n"
            "- D (JWT Bearer Token): JWT Bearer es server-to-server. Requiere certificados y es para sistemas "
            "con capacidad de firmar JWTs. Los sensores IoT simples no tienen esta capacidad criptográfica."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.remoteaccess_asset_token_flow.htm&type=5"
    },
    42: {
        "explanation": (
            "Las respuestas correctas son A y C. Para permitir login a la app móvil con contraseña de Active Directory "
            "sin VPN, se necesitan dos componentes trabajando juntos.\n\n"
            "A (Active Directory Password Sync Plugin): Este plugin se instala en los Domain Controllers de Active Directory "
            "y detecta cambios de contraseña en tiempo real. Cuando un usuario cambia su contraseña en AD, "
            "el plugin sincroniza el hash de la nueva contraseña a Salesforce, permitiendo que Salesforce valide "
            "la contraseña de AD directamente sin necesidad de conexión de red al AD.\n\n"
            "C (Salesforce Identity Connect): Identity Connect maneja la sincronización de usuarios entre AD y Salesforce "
            "(crear, actualizar, desactivar usuarios). Trabaja en conjunto con el Password Sync Plugin para proporcionar "
            "una solución completa de integración AD.\n\n"
            "La combinación A+C permite: Identity Connect sincroniza los usuarios, y el Password Sync Plugin sincroniza "
            "las contraseñas. Los usuarios pueden hacer login directo a Salesforce con su contraseña AD sin VPN.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- B (Trigger on Contact): No existe un mecanismo de trigger en Contact para sincronizar contraseñas. "
            "Es técnicamente inviable e inseguro.\n"
            "- D (Cloud Provider Load Balancer): Un balanceador de carga distribuye tráfico. No resuelve el problema "
            "de autenticación con credenciales de AD."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.identity_connect_basics.htm&type=5"
    },
    43: {
        "explanation": (
            "La respuesta correcta es A (SAML SP + SCIM para provisioning/deprovisioning). "
            "Este escenario tiene dos requisitos claros: SSO via SAML y provisioning/deprovisioning automatizado "
            "disparado por cambios en el IAM central.\n\n"
            "Configurar Salesforce como SAML Service Provider cumple el requisito de SSO. "
            "Habilitar SCIM (System for Cross-domain Identity Management) cumple el requisito de provisioning/deprovisioning "
            "automatizado. SCIM es un estándar REST-based que permite al IAM central enviar comandos a Salesforce para: "
            "crear usuarios (POST), actualizar (PATCH/PUT), desactivar (PATCH con active=false), y eliminar (DELETE).\n\n"
            "SCIM es el estándar de la industria para provisioning cross-domain y es la solución recomendada por Salesforce "
            "cuando un sistema IAM central necesita gestionar el ciclo de vida de usuarios en múltiples aplicaciones cloud.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- B (Auth Provider + Registration Handler): Los Registration Handlers solo se ejecutan durante el login. "
            "No manejan DEPROVISIONING cuando un usuario es desactivado en el IAM sin que intente hacer login.\n"
            "- C (SAML SP + JIT): JIT provisioning solo crea/actualiza usuarios durante el LOGIN. "
            "No puede DEPROVISIONAR usuarios cuando son desactivados en el IAM central (porque el trigger es el login, "
            "y un usuario desactivado no va a intentar hacer login).\n"
            "- D (Identity Connect): Identity Connect es específico para Microsoft Active Directory on-premise. "
            "La pregunta dice 'central cloud-based IAM Service', no AD."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.identity_scim_overview.htm&type=5"
    },
    44: {
        "explanation": (
            "Las respuestas correctas son A y C. Cuando se usa el campo AMR (Authentication Method Reference) "
            "en Login History para verificar MFA con IdPs externos, hay consideraciones importantes.\n\n"
            "A (Dependency on OIDC implementation at IdP): El campo AMR en Salesforce se popula a partir del claim 'amr' "
            "en el ID Token de OpenID Connect. Si el IdP no incluye el claim 'amr' en su implementación OIDC, "
            "el campo estará vacío en Salesforce. Es decir, la utilidad del campo AMR DEPENDE de que el IdP lo soporte.\n\n"
            "C (AMR muestra los métodos de autenticación usados en el IdP): El campo AMR refleja los métodos "
            "que el IdP reporta haber usado para autenticar al usuario (ej: 'pwd' para password, 'mfa' para multi-factor, "
            "'otp' para one-time password). Esto permite al arquitecto de seguridad verificar que los usuarios "
            "están realmente usando MFA en el IdP.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- B (High assurance sessions must be configured): Aunque es una buena práctica, no es una consideración "
            "específica del campo AMR. Las session security levels son una configuración separada.\n"
            "- D (Both OIDC and SAML supported): El campo AMR se popula SOLO desde OIDC (claim 'amr'). "
            "Para SAML, Salesforce usa AuthnContext, no AMR. La opción dice que 'both are supported' para AMR, "
            "lo cual es incorrecto."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.users_login_history_fields.htm&type=5"
    },
    45: {
        "explanation": (
            "La respuesta correcta es D (Añadir un sistema de identidad central que federe entre los sistemas ADFS). "
            "Con tres sistemas ADFS regionales y un solo org de Salesforce, la arquitectura óptima es tener un punto "
            "central de federación.\n\n"
            "Un sistema central de identidad (hub) que federe entre los tres ADFS regionales permite: "
            "una sola configuración SSO en Salesforce (apuntando al hub), routing inteligente de autenticación "
            "al ADFS regional correcto según el usuario, y una experiencia de login uniforme sin que el usuario "
            "deba elegir su región.\n\n"
            "Esto se puede implementar usando: uno de los ADFS existentes como hub (usando Claims Provider Trusts "
            "para conectar los otros), Azure AD como hub federador, u otra solución de federación. "
            "Usar Claims Provider Trusts en ADFS existente NO requiere procurar software adicional.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (Identity Connect): Identity Connect es para sync AD→Salesforce, no para federación entre "
            "múltiples ADFS. Además, ES un producto adicional que requiere inversión.\n"
            "- B (Múltiples SSO configs + user choice): Funciona técnicamente, pero la experiencia de usuario es pobre "
            "(el usuario debe saber cuál ADFS elegir). No es la mejor práctica arquitectural.\n"
            "- C (Connected Apps + Salesforce site): Excesivamente complejo y no es el patrón correcto para SSO. "
            "Las Connected Apps son para apps que usan Salesforce como IdP, no al revés."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.sso_saml.htm&type=5"
    },
    46: {
        "explanation": (
            "Las respuestas correctas son A y D. Para brandear la experiencia de login con logo, colores "
            "y right-frame dinámico en Experience Cloud, hay dos enfoques válidos.\n\n"
            "A (Build custom pages en Experience Cloud): Experience Builder permite crear páginas de login "
            "completamente personalizadas con componentes custom. Puedes diseñar la página con tu logo, "
            "colores de marca, y layouts específicos usando componentes Lightning o custom LWC. "
            "Esto da control total sobre la apariencia.\n\n"
            "D (Login & Registration branded en Community Administration): En la administración de la comunidad "
            "(Workspaces > Administration > Login & Registration), hay opciones nativas para configurar: "
            "logo de la página de login, color de fondo, color del botón de login, y una URL para el right-frame "
            "(que muestra contenido dinámico de una URL externa en el lado derecho de la página de login). "
            "Todo esto es configuración declarativa sin código.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- B (Experience Builder para Reset/Forgot Password): Aunque Experience Builder puede personalizar "
            "estas páginas, la pregunta es sobre la página de LOGIN y sus elementos específicos (logo, colores, right-frame). "
            "Reset/Forgot Password son páginas diferentes.\n"
            "- C (Custom site pages para reset/forgot): Mismo problema - la pregunta es sobre branding del LOGIN page, "
            "no sobre las páginas de recuperación de contraseña."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.networks_customize_login_page.htm&type=5"
    },
    47: {
        "explanation": (
            "Las respuestas correctas son A, B y C. Para permitir self-registration sin asignar automáticamente "
            "un contact hasta verificación, usando External Identity licenses, se necesitan estos tres pasos.\n\n"
            "A (Configurable Self-Reg Page): En Login & Registration settings, seleccionar la opción "
            "'Configurable Self-Reg Page' permite personalizar los campos y el comportamiento de la página "
            "de auto-registro. Es necesario para controlar qué información se recopila.\n\n"
            "B (Customize self-registration handler to create only user): El Self-Registration Handler (clase Apex) "
            "normalmente crea User + Contact + Account. Personalizándolo para crear SOLO el User record "
            "(sin Contact ni Account), el usuario queda como 'guest verificado' sin asociación a registros CRM "
            "hasta que complete el onboarding.\n\n"
            "C (Enable 'Allow customers and partners to self-register'): Este es el switch principal que habilita "
            "la funcionalidad de auto-registro en el site. Sin habilitarlo, no aparece el enlace de registro.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- D (Associate to shared single contact): Asociar todos los usuarios a un solo Contact compartido "
            "es un anti-pattern. Causa problemas de datos, sharing, y reporting.\n"
            "- E (External login page + SF APIs): Crear una página externa es sobre-ingeniería. "
            "Salesforce proporciona la funcionalidad nativa con los pasos A, B, C."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.networks_customize_selfreg.htm&type=5"
    },
    48: {
        "explanation": (
            "La respuesta correcta es B (External Identity License). "
            "Para una aplicación B2C (business-to-consumer) que usa Salesforce Identity para SSO, "
            "la licencia External Identity es la apropiada.\n\n"
            "External Identity es el tipo de licencia diseñado para usuarios EXTERNOS (consumidores/clientes) "
            "que necesitan autenticarse en una aplicación customer-facing. Proporciona: "
            "capacidades de Identity (login, SSO, social sign-in, MFA), acceso a Experience Cloud sites, "
            "self-registration, y profile management, a un costo significativamente menor que licencias Community.\n\n"
            "Para un caso B2C donde los consumidores solo necesitan login/SSO (no acceso completo a CRM), "
            "External Identity es la licencia mínima y más cost-effective.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (Salesforce Platform): Es una licencia para usuarios INTERNOS con acceso a objetos custom. "
            "Demasiado costosa y con funcionalidad innecesaria para consumidores externos.\n"
            "- C (Identity Only): Es para usuarios INTERNOS (empleados) que usan Salesforce como IdP "
            "para acceder a otras apps. No es para usuarios externos B2C.\n"
            "- D (Partner Community): Es para partners comerciales que necesitan acceso a CRM "
            "(Leads, Opportunities, etc.). Excesivo para consumidores que solo necesitan SSO."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.users_license_types_communities.htm&type=5"
    },
    49: {
        "explanation": (
            "La respuesta correcta es A (Login Forensics). "
            "Login Forensics es una herramienta de Salesforce Shield Event Monitoring que proporciona análisis "
            "estadístico avanzado de datos de login para detectar actividad anómala o fraudulenta.\n\n"
            "Login Forensics genera reportes que incluyen exactamente lo que pide la pregunta: "
            "número promedio de logins por usuario, usuarios que exceden el promedio, logins en horas no laborales, "
            "logins desde IPs o ubicaciones inusuales, y patrones de autenticación sospechosos. "
            "Está diseñado para organizaciones grandes (como la de 15,000 empleados) que necesitan "
            "identificar y curb actividad fraudulenta a escala.\n\n"
            "Login Forensics va más allá de Login History porque no solo registra eventos sino que "
            "aplica análisis estadístico para identificar outliers y anomalías.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- B (Login Report): No existe un 'Login Report' como producto o feature específico en Salesforce.\n"
            "- C (Login Inspector): No existe un 'Login Inspector' como herramienta en Salesforce.\n"
            "- D (Login History): Login History es un registro crudo de eventos de login. Muestra datos individuales "
            "pero NO proporciona análisis estadístico (promedios, comparaciones, detección de anomalías). "
            "Para el análisis que pide la pregunta (average number, who logged in more than average, non-business hours), "
            "necesitas Login Forensics que automatiza este análisis."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.security_login_forensics.htm&type=5"
    },
    50: {
        "explanation": (
            "La respuesta correcta es B (secuencia: 4, 1, 5, 2, 3). "
            "El OAuth 2.0 Web Server Flow (Authorization Code Grant) sigue una secuencia específica "
            "que es fundamental entender para el examen.\n\n"
            "La secuencia correcta es:\n"
            "Paso 1 → (4) Request an Authorization Code: La aplicación redirige al usuario al authorization endpoint "
            "de Salesforce (/services/oauth2/authorize) con client_id, redirect_uri y scopes.\n"
            "Paso 2 → (1) User Authenticates and Authorizes Access: Salesforce muestra la página de login. "
            "El usuario ingresa credenciales y autoriza el acceso (consent screen).\n"
            "Paso 3 → (5) Salesforce Grants Authorization Code: Salesforce redirige al callback URL "
            "de la app con un authorization code como parámetro.\n"
            "Paso 4 → (2) Request an Access Token: La app envía el authorization code + client_id + "
            "client_secret al token endpoint (/services/oauth2/token).\n"
            "Paso 5 → (3) Salesforce Grants an Access Token: Salesforce valida y devuelve access_token + refresh_token.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (2,3,4,5,1): Pide token antes del auth code. Imposible sin code.\n"
            "- C (4,5,2,3,1): Omite la autenticación del usuario entre request y grant del code.\n"
            "- D (1,4,5,2,3): Pone autenticación antes de solicitar el code. La solicitud del code "
            "INICIA el proceso (redirige al usuario), y LUEGO el usuario se autentica."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.remoteaccess_oauth_web_server_flow.htm&type=5"
    },
    51: {
        "explanation": (
            "La respuesta correcta es C (La funcionalidad de contactless user solo está disponible con External Identity license). "
            "Este es el impacto arquitectural principal que debe considerarse al implementar contactless users.\n\n"
            "Los Contactless Users son usuarios que se crean sin un registro de Contact asociado. "
            "Esto reduce overhead de gestión porque no necesitas crear Account/Contact para cada usuario registrado. "
            "Sin embargo, la limitación clave es que esta funcionalidad SOLO está disponible con la licencia External Identity.\n\n"
            "Este constraint arquitectural es importante porque la licencia External Identity tiene funcionalidades "
            "limitadas en Experience Cloud comparada con Customer Community o Partner Community licenses. "
            "Los usuarios con External Identity no pueden acceder a todos los objetos CRM, tienen límites de API "
            "diferentes, y no pueden usar algunas funcionalidades avanzadas de Experience Cloud.\n\n"
            "Si NTO planea que estos usuarios eventualmente necesiten acceso completo a la comunidad, "
            "deberán hacer upgrade de licencia, lo cual crea complejidad adicional.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (Custom registration handler): Aunque es verdad que se necesita un handler, esto no es un 'impacto "
            "arquitectural' sino un detalle de implementación normal.\n"
            "- B (Contact auto-created on upgrade): El Contact no se crea automáticamente ni se asocia a un Account "
            "de forma automática durante un upgrade de licencia. Esto requiere configuración adicional.\n"
            "- D (Passwordless incompatible): Passwordless SÍ funciona con contactless users. "
            "El OTP puede enviarse al email/teléfono del User record sin necesidad de Contact."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.networks_contactless_user.htm&type=5"
    },
    52: {
        "explanation": (
            "La respuesta correcta es C (Configurar un OpenID Connect Authentication Provider). "
            "Cuando un proveedor de identidad externo soporta OAuth, la forma de integrarlo con Salesforce "
            "Experience Cloud es a través de un Authentication Provider de tipo OpenID Connect.\n\n"
            "OpenID Connect (OIDC) es una capa de identidad construida sobre OAuth 2.0. "
            "En Salesforce, el tipo de Auth Provider 'OpenID Connect' es la configuración genérica que permite "
            "conectar con cualquier proveedor compatible con OAuth 2.0/OIDC. Solo necesitas configurar: "
            "Consumer Key, Consumer Secret, Authorize Endpoint URL, Token Endpoint URL, y User Info Endpoint URL.\n\n"
            "Esta es la opción correcta porque el proveedor soporta OAuth, y OIDC es la forma estándar de usar "
            "OAuth para autenticación (OAuth solo es para autorización; OIDC añade la capa de identidad).\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (Custom external auth provider): Crear un auth provider custom (implementando interfaces Apex) "
            "es innecesario cuando el tipo genérico 'OpenID Connect' ya soporta cualquier proveedor OAuth/OIDC estándar. "
            "Custom solo se necesita para proveedores con flujos no estándar.\n"
            "- B (Certificate-based auth): La autenticación basada en certificados es para autenticación mutua TLS (mTLS), "
            "no tiene relación con OAuth/OIDC.\n"
            "- D (Delegated SSO): Delegated Authentication usa SOAP webservices y está deprecado. "
            "No es la solución para proveedores OAuth."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.sso_provider_openid_connect.htm&type=5"
    },
    53: {
        "explanation": (
            "Las respuestas correctas son B, D y E. Para implementar User Provisioning a Concur con aprobación previa, "
            "se necesitan tres pasos.\n\n"
            "E (Create Connected App for Concur): Primero, debes crear una Connected App que represente Concur en Salesforce. "
            "Esto establece la relación entre Salesforce y la aplicación externa.\n\n"
            "D (Enable User Provisioning for Connected App): En la Connected App de Concur, "
            "habilitas la funcionalidad de User Provisioning. Esto activa el framework de provisioning "
            "que incluye un provisioning flow y la capacidad de sincronizar usuarios.\n\n"
            "B (Approval process for UserProvisioningRequest): El objeto UserProvisioningRequest es el registro "
            "que se crea cuando el sistema de provisioning determina que un usuario necesita ser creado en la app externa. "
            "Creando un Approval Process sobre este objeto, puedes requerir aprobación antes de que la cuenta "
            "se cree en Concur. Esto cumple el requisito del HR director.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (Approval on User object): El User object es el usuario de Salesforce, no la solicitud de provisioning. "
            "Un approval en User no controlaría la creación de cuentas en Concur.\n"
            "- C (Approval on custom object): No se necesita un custom object. Salesforce ya tiene el objeto estándar "
            "UserProvisioningRequest diseñado exactamente para este propósito."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.connected_app_user_provisioning.htm&type=5"
    },
    54: {
        "explanation": (
            "La respuesta correcta es A (El SP necesita hacer API calls a Salesforce en nombre del usuario). "
            "Esta es LA diferencia clave entre usar OIDC vs SAML cuando Salesforce actúa como Identity Provider.\n\n"
            "Cuando usas OIDC (OpenID Connect): el Service Provider recibe un ID Token (identidad) Y un Access Token "
            "(autorización). Con el Access Token, el SP puede hacer llamadas API a Salesforce en nombre del usuario "
            "que se autenticó. Esto es posible porque OIDC está construido sobre OAuth 2.0.\n\n"
            "Cuando usas SAML: el Service Provider solo recibe una aserción SAML con la identidad del usuario. "
            "NO recibe un token de acceso. El SP puede autenticar al usuario pero NO puede hacer API calls "
            "de vuelta a Salesforce en su nombre.\n\n"
            "Por lo tanto, si el SP necesita acceder a APIs de Salesforce después del login, DEBES usar OIDC. "
            "Si solo necesita autenticación (saber quién es el usuario), ambos funcionan.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- B (OIDC es más seguro que SAML): FALSO. Ambos protocolos son seguros cuando se implementan correctamente. "
            "Tienen diferentes fortalezas pero ninguno es inherentemente más seguro.\n"
            "- C (Son equivalentes): FALSO. Tienen una diferencia fundamental: OIDC proporciona acceso a APIs, SAML no.\n"
            "- D (Session existente evita re-login): Esto aplica a AMBOS protocolos (SSO es SSO). "
            "No es un factor diferenciador entre OIDC y SAML."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.remoteaccess_oidc_overview.htm&type=5"
    },
    55: {
        "explanation": (
            "La respuesta correcta es C (Los créditos se consumen con cada SMS enviado). "
            "Los Identity Verification Credits se consumen SOLO cuando se envían mensajes SMS, "
            "no cuando se envían emails de verificación.\n\n"
            "En el contexto de passwordless login, los usuarios pueden recibir códigos de verificación por email o SMS. "
            "Los emails no consumen créditos (están incluidos en la plataforma). Los SMS SÍ consumen créditos porque "
            "Salesforce paga a carriers de telecomunicaciones por cada mensaje enviado.\n\n"
            "Para estimar la cantidad necesaria: debes calcular cuántos usuarios usarán verificación por SMS "
            "(no email) y con qué frecuencia iniciarán sesión. Por ejemplo, si 10,000 usuarios hacen login "
            "5 veces al mes por SMS = 50,000 créditos/mes necesarios.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (Credits consumed per verification sent): Dice que se consumen 'con cada verificación', "
            "incluyendo email. Esto es INCORRECTO. Solo SMS consume créditos.\n"
            "- B (10,000 credits included per community): No existe este paquete gratuito de 10,000 créditos "
            "por comunidad. Los créditos se compran por separado.\n"
            "- D (Direct add-on based on existing licenses): Los créditos NO se calculan directamente basándose "
            "en el número de licencias existentes. Se estiman basándose en el USO esperado de SMS."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.identity_verification_credits.htm&type=5"
    },
    56: {
        "explanation": (
            "Las respuestas correctas son A y D. Para popular campos custom del User object durante SSO SAML login, "
            "se necesita implementar la interfaz JIT y los métodos de create/update.\n\n"
            "A (Implement Auth.SamlJitHandler Interface): Esta es la interfaz Apex que define los métodos para "
            "Just-in-Time provisioning custom con SAML. Al implementarla, tu clase Apex puede acceder a TODOS "
            "los atributos de la aserción SAML, incluyendo atributos custom que el IdP envía con datos para "
            "los campos personalizados del User object.\n\n"
            "D (Create and Update methods): La interfaz Auth.SamlJitHandler define dos métodos principales: "
            "createUser() y updateUser(). createUser() se ejecuta cuando el usuario no existe en Salesforce (primer login), "
            "y updateUser() se ejecuta en logins subsecuentes. En ambos métodos, puedes mapear atributos SAML "
            "a campos custom del User object (user.Custom_Field__c = attributes.get('customAttribute')).\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- B (RegistrationHandler Interface): RegistrationHandler es para Authentication Providers (OAuth/OIDC), "
            "no para SAML SSO. La pregunta especifica SSO login, que en Salesforce típicamente es SAML.\n"
            "- C (SessionManagement Class): No existe una clase 'SessionManagement' estándar para este propósito. "
            "Session management no tiene relación con el provisioning de datos de usuario durante login."
        ),
        "reference": "https://developer.salesforce.com/docs/atlas.en-us.apexref.meta/apexref/apex_interface_Auth_SamlJitHandler.htm"
    },
    57: {
        "explanation": (
            "La respuesta correcta es B (HTTP POST al revoke token endpoint). "
            "Para invalidar un token OAuth de Salesforce, se usa el endpoint estándar de revocación de tokens.\n\n"
            "Salesforce expone el endpoint /services/oauth2/revoke que acepta un HTTP POST con el token "
            "(access token o refresh token) como parámetro. Al llamar a este endpoint, el token es inmediatamente "
            "invalidado y ya no puede usarse para acceder a APIs. Si revocas un refresh token, "
            "todos los access tokens derivados de él también se invalidan.\n\n"
            "El endpoint acepta: POST /services/oauth2/revoke con body: token=<token_value>. "
            "Devuelve 200 OK si la revocación fue exitosa.\n\n"
            "Este es el mecanismo estándar OAuth 2.0 (RFC 7009) para revocación de tokens y es la forma correcta "
            "de implementar logout desde una aplicación externa.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (POST a SCIM endpoint): SCIM es para provisioning de usuarios, no para revocar tokens OAuth. "
            "Los endpoints SCIM gestionan User records, no sesiones.\n"
            "- C (Single Logout con logout URL): SLO es para SAML SSO (termina sesiones SAML). "
            "No es el mecanismo para revocar tokens OAuth.\n"
            "- D (POST para request refresh token): Solicitar un refresh token es lo OPUESTO a revocar. "
            "Obtener un nuevo refresh token no invalida el anterior."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.remoteaccess_revoke_token.htm&type=5"
    },
    58: {
        "explanation": (
            "La respuesta correcta es B (OAuth 2.0 Asset Token Flow). "
            "El escenario describe un dispositivo (fitness tracker) que, después de ser registrado por el usuario, "
            "necesita crear Cases automáticamente en Salesforce cuando detecta problemas.\n\n"
            "El Asset Token Flow es diseñado para este caso exacto: un dispositivo IoT que ha sido registrado "
            "por un usuario y necesita actuar autónomamente en nombre de ese usuario. El flujo funciona:\n"
            "1. El usuario compra y registra el dispositivo (se crea un Asset en Salesforce vinculado a su Account)\n"
            "2. El dispositivo recibe un token derivado (actor token) durante el registro\n"
            "3. Cuando el dispositivo detecta un problema, usa su actor token para obtener un access token\n"
            "4. Con el access token, crea un Case asociado al Account del usuario\n\n"
            "El dispositivo actúa 'on behalf of' el usuario sin requerir interacción humana cada vez.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (Device Flow): Device Flow es para la AUTORIZACIÓN INICIAL del dispositivo por parte del usuario. "
            "No es para la operación autónoma posterior del dispositivo.\n"
            "- C (User-Agent Flow): Requiere un navegador y interacción del usuario. Un fitness tracker "
            "que envía alertas automáticas no puede usar este flujo.\n"
            "- D (SAML Bearer): SAML Bearer es para integración entre sistemas enterprise que usan SAML. "
            "No es apropiado para dispositivos IoT."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.remoteaccess_asset_token_flow.htm&type=5"
    },
    59: {
        "explanation": (
            "La respuesta correcta es A (OpenID Connect). "
            "Cuando el requisito es devolver atributos de usuario en un ID Token a una aplicación externa, "
            "OpenID Connect es el mecanismo correcto.\n\n"
            "OpenID Connect (OIDC) es una capa de identidad sobre OAuth 2.0 que define el concepto de ID Token. "
            "El ID Token es un JWT (JSON Web Token) que contiene claims (atributos) sobre el usuario autenticado: "
            "sub (subject/user ID), name, email, y cualquier atributo custom configurado. "
            "La aplicación wellness puede decodificar este token para obtener los datos del empleado.\n\n"
            "Cuando Salesforce actúa como OIDC Provider (IdP), puede incluir atributos personalizados del usuario "
            "en el ID Token a través de custom claims, configurados en el Connected App o mediante un Token Handler.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- B (User Agent Flow): Es un tipo de flujo OAuth, no un mecanismo de autenticación. "
            "Puede usar OIDC si se incluye el scope 'openid', pero por sí solo no garantiza el ID Token.\n"
            "- C (Web Server Flow): Igual que B, es un tipo de flujo. Puede incluir OIDC pero la respuesta "
            "específica al requisito de 'ID Token con atributos' es OIDC.\n"
            "- D (JWT Bearer Token Flow): Es server-to-server sin interacción del usuario. "
            "No genera un ID Token con atributos del usuario para la app externa."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.remoteaccess_oidc_overview.htm&type=5"
    },
    60: {
        "explanation": (
            "La respuesta correcta es A (Connected App and OAuth Scopes). "
            "Para integrar una aplicación externa con la API de Salesforce usando OAuth 2.0, "
            "se necesita una Connected App con OAuth Scopes definidos.\n\n"
            "Una Connected App es el mecanismo principal en Salesforce para habilitar acceso OAuth a APIs. "
            "Al crear la Connected App, defines: los OAuth Scopes permitidos (api, web, full, etc.), "
            "la callback URL, y otras políticas de seguridad. Los OAuth Scopes determinan qué puede hacer "
            "la app (api scope permite REST/SOAP API access, web scope permite acceso web, etc.).\n\n"
            "El flujo es: la order fulfillment app se autentica vía OAuth (web server flow o JWT), "
            "obtiene un access token con los scopes autorizados, y usa ese token para consultar order data "
            "a través de la REST/SOAP API.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- B (OAuth Tokens): Los tokens son el RESULTADO del proceso OAuth, no la CONFIGURACIÓN necesaria. "
            "Sin una Connected App, no puedes obtener tokens.\n"
            "- C (Canvas App Integration): Canvas es para embeber apps dentro de Salesforce UI. "
            "La pregunta es sobre una app EXTERNA accediendo a la API de Salesforce.\n"
            "- D (Authentication Providers): Los Auth Providers son para que usuarios ENTREN a Salesforce "
            "desde proveedores externos. La pregunta es lo opuesto: una app externa ACCEDIENDO a Salesforce API."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.connected_app_overview.htm&type=5"
    },
    61: {
        "explanation": (
            "Las respuestas correctas son A y C. Para usar Salesforce como IdP con la billing app accesible "
            "desde Salesforce (con redirect aceptable), se necesitan App Launcher y Connected Apps.\n\n"
            "C (Connected Apps): Para configurar SSO con Salesforce como IdP hacia la billing app, "
            "debes crear una Connected App que represente la billing app. La Connected App puede configurarse "
            "con SAML o OAuth para proporcionar SSO, definiendo cómo Salesforce autentica al usuario "
            "para la app externa.\n\n"
            "A (App Launcher): El App Launcher es la interfaz en Salesforce donde los usuarios ven tiles "
            "de todas las aplicaciones disponibles. Al configurar la Connected App con un StartURL y hacerla "
            "visible en App Launcher, los usuarios pueden acceder a la billing app directamente desde Salesforce "
            "con un click (el redirect que mencionan como aceptable).\n\n"
            "Juntos: Connected App proporciona el SSO, y App Launcher proporciona el acceso desde Salesforce.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- B (Identity Connect): Identity Connect es para sincronización con Active Directory, "
            "no para SSO con aplicaciones externas ni para hacer apps accesibles desde Salesforce.\n"
            "- D (Salesforce Canvas): Canvas embebe apps DENTRO de la UI de Salesforce (inline, no redirect). "
            "La pregunta dice 'A redirect is acceptable', sugiriendo que no necesitan la integración inline de Canvas."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.connected_app_overview.htm&type=5"
    },
    62: {
        "explanation": (
            "La respuesta correcta es B (Implement Experience ID en el código y extender URLs y endpoints). "
            "Experience ID (expid) es el mecanismo nativo de Salesforce para dynamic branding en un mismo "
            "Experience Cloud site sin necesidad de licencias adicionales.\n\n"
            "El Experience ID permite que una sola comunidad muestre diferentes apariencias (logos, colores, imágenes) "
            "según un parámetro en la URL. Cuando los emails promocionales incluyen links con ?expid=sportswear_brand, "
            "la comunidad renderiza con el branding de la nueva marca. Sin el parámetro, muestra el branding NTO default.\n\n"
            "Esto cumple todos los requisitos: dynamic branding basado en el link clickeado, fallback a NTO branding, "
            "no requiere licencias adicionales, y el equipo de desarrollo puede implementar los cambios en el código.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (Heroku + Embedded Login): Construir un nuevo site en Heroku requiere infraestructura adicional "
            "y posiblemente licencias de Heroku. No es necesario cuando expid resuelve el problema.\n"
            "- C (Additional community site): Crear otro sitio requiere configuración, potencialmente licencias "
            "adicionales, y duplica esfuerzo de mantenimiento. La pregunta dice 'no time to procure additional licenses'.\n"
            "- D (Full sandbox): Crear un sandbox y replicar el portal es excesivo, costoso, y no es una solución "
            "de producción para dynamic branding."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.networks_login_page_branding.htm&type=5"
    },
    63: {
        "explanation": (
            "Las respuestas correctas son A, B y C. Estas tres opciones cumplen los criterios de Salesforce para MFA seguro.\n\n"
            "A (Username/password + Security Key): Las llaves de seguridad (FIDO U2F/WebAuthn como YubiKey) "
            "son uno de los métodos MFA más seguros reconocidos por Salesforce. Son resistentes a phishing "
            "porque requieren presencia física del hardware.\n\n"
            "B (Third-party SSO with Mobile Authenticator): Cuando un IdP externo usa una app autenticadora móvil "
            "(como Google Authenticator, Microsoft Authenticator, o Salesforce Authenticator) como segundo factor, "
            "esto cumple los requisitos de MFA. Las apps TOTP generan códigos temporales criptográficamente seguros.\n\n"
            "C (Lightning Login): Lightning Login usa la app Salesforce Authenticator para login basado en "
            "notificaciones push. El usuario recibe una notificación en su teléfono y aprueba con biometría. "
            "Esto cumple MFA porque combina algo que tienes (teléfono) con algo que eres (biometría) o algo que sabes (PIN).\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- D (SMS passcode): Salesforce NO reconoce SMS como método MFA válido desde febrero 2022. "
            "SMS es vulnerable a SIM swapping, interceptación, y otros ataques. Fue eliminado como opción MFA.\n"
            "- E (Email Verification Code): Email NO cumple criterios MFA de Salesforce porque el acceso al email "
            "no constituye un factor de posesión fuerte (puede estar comprometido si la contraseña está comprometida)."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.mfa_overview.htm&type=5"
    },
    64: {
        "explanation": (
            "La respuesta correcta es A (OpenID Connect Token Introspection). "
            "Token Introspection es el mecanismo estándar para verificar el estado (activo/inactivo) de un access token.\n\n"
            "El Token Introspection endpoint (RFC 7662) permite a una aplicación enviar un token y recibir información "
            "sobre su estado: si está activo, cuándo expira, qué scopes tiene, a qué usuario pertenece, etc. "
            "En Salesforce, el endpoint es /services/oauth2/introspect.\n\n"
            "Para una app móvil conectada via OIDC, Token Introspection es la forma correcta de verificar "
            "si un access token sigue siendo válido sin necesidad de intentar una API call.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- B (OIDC Discovery endpoint): El discovery endpoint (.well-known/openid-configuration) devuelve "
            "información sobre la configuración del OIDC provider (endpoints, scopes soportados, etc.). "
            "NO devuelve información sobre tokens específicos.\n"
            "- C (CORS for token endpoint): CORS permite que un navegador haga requests cross-origin. "
            "Es una configuración de seguridad del navegador, no un mecanismo para verificar estado de tokens.\n"
            "- D (Custom OAuth scope): Los scopes definen permisos de acceso. Crear un scope custom "
            "no proporciona información sobre el estado de un token."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.remoteaccess_oidc_token_introspection_endpoint.htm&type=5"
    },
    65: {
        "explanation": (
            "La respuesta correcta es D (Login Flow que condicionalmente muestra prompts). "
            "Para forzar a los usuarios a revisar reglas y actualizar información ANTES de poder usar el portal, "
            "un Login Flow con lógica condicional es la solución ideal.\n\n"
            "Los Login Flows se ejecutan después de la autenticación pero ANTES de que el usuario llegue a la homepage. "
            "Puedes crear un Flow que: 1) Verifica si el usuario ha aceptado las reglas actuales (checkea un campo custom), "
            "2) Si no las ha aceptado, muestra una screen con las reglas y botón de aceptar, "
            "3) Verifica si la información del contacto está completa/actualizada, "
            "4) Si hay datos faltantes/outdated, muestra un formulario para actualizar. "
            "Solo después de completar estos pasos el usuario accede al portal.\n\n"
            "La key word es 'conditionally' - el flow solo muestra las pantallas a usuarios que NO han completado "
            "estos requisitos, permitiendo un login fluido para quienes ya están en compliance.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (Landing page + email campaign): No es obligatorio - el usuario puede ignorar emails y la landing page.\n"
            "- B (Banner en homepage): Un banner es informativo pero no FUERZA la acción. Los usuarios pueden ignorarlo.\n"
            "- C (Tasks): Las tasks son sugerencias, no bloqueos. El usuario puede acceder al portal sin completar tasks."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.security_login_flow.htm&type=5"
    },
    66: {
        "explanation": (
            "Las respuestas correctas son B, C y D. Para habilitar self-registration usando Person Accounts "
            "en Experience Cloud, se requieren tres configuraciones específicas.\n\n"
            "B (Enable Person Accounts): Person Accounts deben estar habilitadas en la org. "
            "Una vez habilitadas, permiten crear Account records que representan personas individuales "
            "(sin Contact separado). Es un prerequisito fundamental.\n\n"
            "C (Default Account field empty): En Login & Registration settings, el campo 'Default Account' "
            "debe estar VACÍO. Cuando está vacío y Person Accounts están habilitadas, el sistema "
            "automáticamente crea Person Accounts para usuarios que se auto-registran, en lugar de "
            "asignarlos a una Business Account existente.\n\n"
            "D (Enable Person and Business Account record types in Public Access Settings): "
            "El site guest user profile necesita acceso a los record types de Person Account y Business Account. "
            "Sin esto, el proceso de self-registration no puede crear Person Account records.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (Enable Business Accounts): Business Accounts ya están habilitadas por defecto. "
            "Lo que necesitas habilitar específicamente son PERSON Accounts.\n"
            "- E (OWD Contact = Public Read Only): Los Organization-Wide Defaults para Contact no son relevantes "
            "para Person Accounts porque Person Accounts NO tienen Contact record separado. "
            "Además, cambiar OWDs tiene implicaciones amplias de seguridad."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.networks_customize_selfreg.htm&type=5"
    },
    67: {
        "explanation": (
            "La respuesta correcta es A (Experience ID como URL parameter en OAuth/OIDC y SAML flows). "
            "Para una solución multi-branded CIAM en la plataforma Salesforce, "
            "el Experience ID es el mecanismo oficial para asegurar la experiencia de marca correcta.\n\n"
            "El Experience ID (expid) se incluye como parámetro en las URLs de los flujos de autenticación: "
            "- OAuth: /services/oauth2/authorize?client_id=...&expid=brand_value "
            "- SAML: se incluye en el RelayState o como parámetro "
            "Salesforce usa este valor para determinar qué configuración de branding aplicar "
            "(logos, colores, textos, layouts) en la experiencia de login y registro.\n\n"
            "Esta es la forma recomendada por Salesforce para multi-brand en una sola comunidad "
            "porque no requiere múltiples sitios ni desarrollo custom extenso.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- B (Audience ID en cookie): No existe un mecanismo de 'Audience ID en shared cookie' "
            "para branding en Salesforce. Las cookies no se usan para este propósito.\n"
            "- C (Custom parameter + login page logic): Aunque técnicamente posible, requiere desarrollo custom "
            "de la lógica en la login page. El Experience ID es la solución nativa sin custom code.\n"
            "- D (Brand picker por el usuario): Pedir al usuario que seleccione su marca es mala UX. "
            "El sistema debe saber automáticamente qué marca mostrar basándose en cómo llegó el usuario."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.networks_login_page_branding.htm&type=5"
    },
    68: {
        "explanation": (
            "La respuesta correcta es D (Partners register through IdP, create users in SF via API). "
            "Cuando hay un IdP externo y se necesita evitar duplicados, la fuente de verdad para el registro "
            "debe ser el IdP, y la creación en Salesforce se hace vía API.\n\n"
            "Este enfoque funciona así: 1) El partner se registra en el IdP externo (que verifica que no existe duplicado), "
            "2) El IdP notifica a Salesforce vía API para crear el Partner User, "
            "3) El IdP mantiene el control de identidades únicas, evitando duplicados.\n\n"
            "El IdP como punto central de registro garantiza unicidad porque es la autoridad de identidades. "
            "Si se registraran en Salesforce Y en el IdP por separado, habría riesgo de inconsistencias.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (Custom page in Experience Cloud for both systems): Crear registros en dos sistemas desde "
            "una sola página es complejo y propenso a errores. Si falla la creación en uno de los dos sistemas, "
            "queda inconsistente.\n"
            "- B (Self-register in EC, then create in Ping): Este orden (SF primero, IdP después) puede crear "
            "usuarios en SF que fallan al crearse en el IdP, generando inconsistencias.\n"
            "- C (Custom web page + APIs for both): Similar a A - crear en dos sistemas simultáneamente "
            "es propenso a errores de consistencia. Mejor tener una fuente autoritativa (el IdP)."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.networks_auth_providers.htm&type=5"
    },
    69: {
        "explanation": (
            "La respuesta correcta es A (Expiración o revocación del access token del IdP). "
            "Cuando usuarios reportan logouts intermitentes con OAuth SSO, la causa más probable "
            "es que el access token expire o sea revocado.\n\n"
            "En un flujo OAuth SSO, el access token tiene un tiempo de vida limitado (TTL). "
            "Cuando expira, la sesión se termina y el usuario debe re-autenticarse. "
            "Si el TTL es corto o variable, los usuarios experimentarán logouts 'intermitentes'. "
            "También puede ocurrir si el IdP revoca tokens por políticas de seguridad.\n\n"
            "Los síntomas de 'intermittent logouts' son consistentes con token expiration porque: "
            "- Ocurre después de un período de tiempo (no inmediatamente) "
            "- Afecta a usuarios de forma inconsistente (depende de cuándo hicieron login) "
            "- Se resuelve al volver a autenticarse\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- B (Misconfigured device/browser): Si fuera un problema de dispositivo, el usuario tendría problemas "
            "CONSTANTES, no intermitentes. Además, esto causaría error de conexión, no logout.\n"
            "- C (Network routing delays): Los delays de red causan timeouts o páginas lentas, no logouts. "
            "Una vez establecida la sesión, la latencia no causa desconexión.\n"
            "- D (Insufficient permissions): Permisos insuficientes causan errores de acceso (403), "
            "no logouts. El usuario vería 'Insufficient Privileges' en lugar de ser desconectado."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.remoteaccess_oauth_tokens_scopes.htm&type=5"
    },
    70: {
        "explanation": (
            "La respuesta correcta es D (Cuando un usuario es desaprovisionado en AD on-premise, "
            "la sesión de Salesforce se revoca inmediatamente). "
            "Esta es la feature clave de Identity Connect para integración con Active Directory.\n\n"
            "Identity Connect monitorea cambios en Active Directory en tiempo real. Cuando un administrador "
            "deshabilita o elimina una cuenta en AD (deprovisioning), Identity Connect puede inmediatamente "
            "desactivar al usuario en Salesforce Y revocar sus sesiones activas. Esto es crítico para seguridad: "
            "si un empleado es despedido, su acceso a Salesforce se revoca en segundos, no en horas.\n\n"
            "Esta revocación inmediata de sesión es una diferencia clave respecto a otros métodos de deprovisioning "
            "(como SCIM) que pueden tener latencia.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (Managed package on SF org): FALSO. Identity Connect NO es un managed package de Salesforce. "
            "Es una aplicación Java que se instala ON-PREMISE, cerca del Active Directory. "
            "No se ejecuta en la plataforma Salesforce.\n"
            "- B (Acts as IdP for both): FALSO. Identity Connect NO es un Identity Provider. "
            "Es un middleware de sincronización. Puede facilitar SSO pero no ACTÚA como IdP.\n"
            "- C (Disables users in FIFO): FALSO. Identity Connect no tiene lógica FIFO para licencias. "
            "Si se exceden licencias, genera un error/alerta, no deshabilita usuarios existentes arbitrariamente."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.identity_connect_basics.htm&type=5"
    },
    71: {
        "explanation": (
            "La respuesta correcta es C (Identity Only License). "
            "Para usar Salesforce como Identity Provider para empleados que no necesitan CRM, "
            "la licencia Identity Only es la apropiada y más económica.\n\n"
            "La licencia Identity Only está diseñada para usuarios que SOLO necesitan Salesforce como hub de identidad. "
            "Proporciona: acceso al App Launcher, Single Sign-On a aplicaciones externas, "
            "Multi-Factor Authentication, gestión de sesiones, y acceso a Connected Apps. "
            "NO proporciona acceso a objetos CRM (Accounts, Contacts, Opportunities, Cases, etc.).\n\n"
            "En este escenario, UC ya tiene Sales Team con licencias completas que usan el CRM. "
            "Para los demás empleados que solo necesitan usar Salesforce como IdP para hacer SSO "
            "a portales internos, Identity Only es suficiente y cost-effective.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (Identity Verification): No es un tipo de licencia de usuario. Son créditos para SMS verification.\n"
            "- B (Identity Connect): Es un producto de software (middleware AD), no una licencia de usuario.\n"
            "- D (External Identity): Es para usuarios EXTERNOS (clientes, consumidores en Experience Cloud). "
            "Los empleados internos necesitan Identity Only, no External Identity."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.users_license_types_available.htm&type=5"
    },
    72: {
        "explanation": (
            "La respuesta correcta es D (SAML Assertion Validator). "
            "Cuando un administrador tiene problemas configurando SSO con un IdP externo, "
            "el SAML Assertion Validator es la herramienta específica para troubleshooting.\n\n"
            "El SAML Assertion Validator es una herramienta en Setup > Single Sign-On Settings que permite "
            "pegar una aserción SAML raw (capturada del navegador o proporcionada por el IdP) y validarla "
            "contra la configuración SSO de Salesforce. La herramienta identifica exactamente qué está mal: "
            "firma inválida, issuer incorrecto, ACS URL mismatch, assertion expirada, subject format incorrecto, etc.\n\n"
            "Es la herramienta MÁS específica para 'trouble getting things configured' porque analiza "
            "la aserción SAML y la compara contra tu configuración, mostrando discrepancias.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (Login History): Muestra que hubo un error, pero no detalla QUÉ está mal en la configuración. "
            "Es útil después de tener una configuración parcial, no durante la configuración inicial.\n"
            "- B (Setup Audit Trail): Muestra cambios de configuración realizados, no errores de autenticación. "
            "Útil para ver qué se cambió, pero no para diagnosticar problemas SSO.\n"
            "- C (Debug Logs): Solo útiles si hay código Apex involucrado (JIT handlers). "
            "El proceso SAML básico no genera debug logs útiles para configuración."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.sso_saml_validation_errors.htm&type=5"
    },
    73: {
        "explanation": (
            "La respuesta correcta es A (Revisar Login History para detalles del error). "
            "Para errores SAML SSO intermitentes que ya están ocurriendo en producción, "
            "Login History es el primer punto de investigación.\n\n"
            "Login History registra CADA intento de login, incluyendo los fallidos por SSO. Para errores SAML, "
            "muestra: el tipo de error específico (Assertion Expired, Replay Detected, Invalid Signature, etc.), "
            "la hora exacta, el usuario afectado, y el IdP que envió la aserción. "
            "Con errores INTERMITENTES, Login History permite ver patrones: ¿ocurre a ciertas horas? "
            "¿afecta a ciertos usuarios? ¿el error cambia?\n\n"
            "La diferencia con Q72 es el contexto: Q72 es sobre configuración inicial (SAML Assertion Validator). "
            "Q73 es sobre errores intermitentes en producción (Login History para análisis de patrones).\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- B (SAML Assertion Validator): Útil para validar una aserción específica, pero para errores "
            "intermitentes necesitas primero ver el PATRÓN en Login History.\n"
            "- C (Check SSO settings and certificate): Si la configuración estuviera mal, los errores serían "
            "CONSTANTES, no intermitentes. Una configuración errónea causa fallos 100% del tiempo.\n"
            "- D (SAML debug logging): Puede ser útil como segundo paso, pero Login History es más rápido "
            "y muestra la información necesaria para errores intermitentes."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.users_login_history.htm&type=5"
    },
    74: {
        "explanation": (
            "La respuesta correcta es C (Configurar la aserción SAML para incluir AuthnContext con la referencia "
            "de clase MFA apropiada). Esto permite que Salesforce reconozca que el usuario ya completó MFA en el IdP.\n\n"
            "AuthnContext (Authentication Context) es un elemento de la aserción SAML que comunica cómo "
            "se autenticó el usuario en el IdP. Cuando el IdP incluye una AuthnContextClassRef que indica MFA "
            "(ej: urn:oasis:names:tc:SAML:2.0:ac:classes:PasswordProtectedTransport para password, "
            "o una clase custom que indica MFA), Salesforce puede mapear esto a un nivel de seguridad de sesión.\n\n"
            "En Salesforce, Setup > Session Settings > Session Security Levels permite definir qué "
            "AuthnContextClassRef values corresponden a 'High Assurance'. Cuando una aserción SAML llega "
            "con un AuthnContext mapeado a High Assurance, la sesión se marca como high-assurance "
            "y el usuario no necesita completar MFA adicional en Salesforce.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (Session Security Level Policies): Aunque necesitas configurar esto EN CONJUNTO con C, "
            "la pregunta es sobre el MECANISMO para que Salesforce reconozca el MFA del IdP. "
            "Ese mecanismo es el AuthnContext en la aserción SAML.\n"
            "- B (Require SF Authenticator for all): Esto haría que los usuarios hagan MFA DOS VECES (IdP + SF). "
            "El objetivo es reconocer el MFA del IdP, no duplicarlo.\n"
            "- D (Login Flows para re-verificar): Igual que B, esto duplicaría la verificación MFA."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.security_auth_high_assurance_session.htm&type=5"
    },
    75: {
        "explanation": (
            "La respuesta correcta es A (Configurar Single Logout (SLO) en las SAML SSO settings). "
            "Single Logout es el mecanismo SAML estándar para propagar el logout entre SP e IdP.\n\n"
            "SAML Single Logout (SLO) funciona así: cuando un usuario hace logout en Salesforce (SP), "
            "Salesforce envía un LogoutRequest al IdP. El IdP procesa el request, termina la sesión del usuario, "
            "y opcionalmente propaga el logout a otros SPs. Esto garantiza que cerrar sesión en un sistema "
            "cierra sesión en todos los sistemas federados.\n\n"
            "En Salesforce, SLO se configura en Setup > Single Sign-On Settings, habilitando "
            "'Single Logout Enabled' y configurando el Single Logout Endpoint URL del IdP. "
            "También se configura el certificado para firmar los LogoutRequests.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- B (Custom logout page redirecting to IdP): Aunque técnicamente posible, es una solución custom "
            "que reimplementa lo que SLO hace nativamente. Además, no maneja todos los edge cases "
            "(como back-channel logout notifications) que el protocolo SLO sí maneja.\n"
            "- C (Login Flow para logout): Los Login Flows se ejecutan durante el LOGIN, no durante el LOGOUT. "
            "No pueden interceptar ni gestionar el proceso de cierre de sesión.\n"
            "- D (IdP monitors SF cookies): Un IdP no puede ni debe monitorear cookies de Salesforce. "
            "Las cookies son específicas del dominio y no pueden leerse cross-domain."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.sso_saml_single_logout.htm&type=5"
    },
    76: {
        "explanation": (
            "La respuesta correcta es B (OAuth 2.0 Web Server Flow). "
            "Para una aplicación web (browser-based) que necesita acceder a APIs de Salesforce en nombre del usuario "
            "sin requerir que re-ingrese credenciales, el Web Server Flow es el más apropiado y seguro.\n\n"
            "El Web Server Flow (Authorization Code Grant) es el flujo OAuth recomendado para aplicaciones web "
            "server-side porque: 1) El client_secret se almacena de forma segura en el servidor "
            "(nunca se expone al navegador), 2) El authorization code es de corta vida y se intercambia server-side, "
            "3) Devuelve un refresh token que permite obtener nuevos access tokens sin re-autenticación del usuario, "
            "4) Es el flujo más seguro para web apps según OAuth 2.0 best practices.\n\n"
            "El usuario se autentica una vez, autoriza la app, y posteriormente la app puede acceder a APIs "
            "usando refresh tokens sin que el usuario vuelva a ingresar credenciales.\n\n"
            "¿Por qué las otras opciones son incorrectas?\n"
            "- A (JWT Bearer Flow): Es server-to-server sin interacción del usuario. No es para apps donde "
            "el usuario necesita autenticarse inicialmente en un navegador.\n"
            "- C (User-Agent Flow): Es para client-side apps (SPA, mobile). Es menos seguro que Web Server Flow "
            "porque el token se expone en la URL/browser. Web Server Flow es superior para web apps con server.\n"
            "- D (Device Flow): Es para dispositivos sin navegador completo (IoT, TV). "
            "La app ya tiene un navegador web, por lo que no necesita Device Flow."
        ),
        "reference": "https://help.salesforce.com/s/articleView?id=sf.remoteaccess_oauth_web_server_flow.htm&type=5"
    },
}


def main():
    # Read existing JSON
    json_path = os.path.join(BASE_DIR, "_clean_questions.json")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Apply corrections and explanations
    for q in data["questions"]:
        qid = q["id"]

        # Apply corrections
        if qid in CORRECTIONS:
            for key, value in CORRECTIONS[qid].items():
                q[key] = value

        # Add explanation
        if qid in EXPLANATIONS:
            q["explanation"] = EXPLANATIONS[qid]["explanation"]
            q["reference"] = EXPLANATIONS[qid]["reference"]

    # Update version
    data["version"] = 2
    data["description"] = "Salesforce Identity & Access Management Architect - Question Bank with Verified Answers and Explanations"

    # Write output
    out_path = os.path.join(BASE_DIR, "_clean_questions_explained.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Output: {out_path}")
    print(f"Total questions: {len(data['questions'])}")
    print(f"With explanations: {sum(1 for q in data['questions'] if 'explanation' in q)}")
    print(f"Corrections applied: {len(CORRECTIONS)} (Q{', Q'.join(str(k) for k in CORRECTIONS)})")


if __name__ == "__main__":
    main()

