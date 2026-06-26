# Salesforce IAM Architect Study Guide (2026)

This document keeps questions and answers in English, and provides the detailed explanation in Spanish.

## Question 1
**Concept:** Community (Partner and Customer) (18%)

**Question (EN):** Universal Containers (UC) has decided to replace the homegrown customer portal with Salesforce Experience Cloud. UC will continue to use its third-party single sign-on (SSO) solution that stores all of its customer and partner credentials. The first time a customer logs in to the Experience Cloud site through SSO, a user record needs to be created automatically. Which solution should an identity architect recommend in order to automatically provision users in Salesforce upon login?

**Correct Answer:** D

**Detailed Explanation (ES):**
La respuesta correcta es **D** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. En Experience Cloud la clave es alinear login, registro y experiencia de usuario con capacidades nativas como Login Discovery, self-registration controlada y branding dinamico. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.networks_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_external

## Question 2
**Concept:** Identity Management Concepts (17%)

**Question (EN):** Universal Containers (UC) is considering a Customer 360 initiative to gain a single source of the truth for its customer data across disparate systems and services. UC wants to understand the primary benefits of Customer 360 Identity and how It contributes to a successful Customer 360 Truth project. What are two are key benefits of Customer 360 Identity as it relates to Customer 360? Customer 3 Ider ete + -- 60 1 .,)Itity enables an organization to build a single login for each of its « ace™ers, giving the organization an understanding of the user's login tivity across all its digital properties and applications. tgey

**Correct Answer:** AD

**Detailed Explanation (ES):**
La respuesta correcta es **AD** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. Esta pregunta exige seleccionar exactamente **2** opciones; la combinacion propuesta respeta esa cardinalidad y evita sobreseleccion o subseleccion. A nivel de conceptos de gestion de identidad, la opcion correcta suele ser la que respeta el flujo estandar de autenticacion/autorizacion y el principio de minimo privilegio. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.identity_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_basics

## Question 3
**Concept:** Accepting Third-Party Identity in Salesforce (21%)

**Question (EN):** Universal Containers is designing an identity architecture that involves integrating Salesforce with an external directory service. The external directory service will act as the central repository for user authentication and authorization across multiple systems within the organization. Which approach should be evaluated to establish trust between Salesforce and the external directory service? AO Utilizing email-based verification for user authentication across the systems. BO Using a shared database table to synchronize user credentials between the two systems. €.© Enforcing IP-based access restrictions for Salesforce and the external directory service. ©) Implementing a federated identity solution based on SAML (Security Assertion Markup Language). Press the "Prnt Scrn” on vour kevboard to take a

**Correct Answer:** A

**Detailed Explanation (ES):**
La respuesta correcta es **A** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. En este dominio suele primar la federacion estandar (SAML/OAuth/OIDC), el aprovisionamiento correcto y la minimizacion de logica custom cuando existe una capacidad nativa de plataforma. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.identity_provider_intro.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_login

## Question 4
**Concept:** Identity Management Concepts (17%)

**Question (EN):** An insurance company has a connected app in its Salesforce environment that is used to integrate with a Google Workspace (formerly known as G Suite). An identity and access management (IAM) architect has been asked to implement automation to enable users, freeze/suspend users, disable users, and reactivate existing users in Google Workspace upon similar actions in | Which solution is recommended to meet this requirement?

**Correct Answer:** D

**Detailed Explanation (ES):**
La respuesta correcta es **D** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. A nivel de conceptos de gestion de identidad, la opcion correcta suele ser la que respeta el flujo estandar de autenticacion/autorizacion y el principio de minimo privilegio. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.identity_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_basics

## Question 5
**Concept:** Salesforce as an Identity Provider (17%)

**Question (EN):** Universal Containers (UC) currently uses Salesforce Sales Cloud and an external billing application. Both Salesforce and the billing application are accessed several times a day to manage customers, UC would like to configure single sign-on and leverage Salesforce as the identity provider. Additionally, UC would like the billing application to be accessible from Salesforce. A redirect is acceptable. Which two Salesforce tools should an identity architect recommend to satisfy the requirements?

**Correct Answer:** AD

**Detailed Explanation (ES):**
La respuesta correcta es **AD** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. Esta pregunta exige seleccionar exactamente **2** opciones; la combinacion propuesta respeta esa cardinalidad y evita sobreseleccion o subseleccion. Cuando Salesforce actua como IdP, la decision correcta normalmente depende del protocolo requerido por el SP y del tipo de token/assertion que necesita la aplicacion consumidora. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.sso_provider_enable.htm&type=5
- https://help.salesforce.com/s/articleView?id=sf.sso_saml.htm&type=5

## Question 6
**Concept:** Accepting Third-Party Identity in Salesforce (21%)

**Question (EN):** Northern Trail Outfitters (NTO) leverages Microsoft Active Directory (AD) for management of employee usernames, passwords, permissions, and asset access. NTO also owns a third-party single sign-on (SSO) solution. The third-party party SSO solution is used for all corporate applications, including Salesforce. NTO has asked an architect to explore Salesforce Identity Connect for automatic provisioning and deprovisioning of users in Salesforce. What role does identity Connect play in the outlined requirements?

**Correct Answer:** AD

**Detailed Explanation (ES):**
La respuesta correcta es **AD** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. Esta pregunta exige seleccionar exactamente **2** opciones; la combinacion propuesta respeta esa cardinalidad y evita sobreseleccion o subseleccion. En este dominio suele primar la federacion estandar (SAML/OAuth/OIDC), el aprovisionamiento correcto y la minimizacion de logica custom cuando existe una capacidad nativa de plataforma. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.identity_provider_intro.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_login

## Question 7
**Concept:** Access Management Best Practices (15%)

**Question (EN):** Northern Trail Outfitters (NTO) is planning to build a new customer service portal and wants to use passwordless login, allowing customers to login with a one-time passcode sent to them via email or SMS. How should the quantity of required Identity Verification Credits be estimated?

**Correct Answer:** A

**Detailed Explanation (ES):**
La respuesta correcta es **A** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. Desde buenas practicas de acceso, se prioriza reducir superficie de riesgo, mantener trazabilidad de autenticacion y aplicar controles estandar antes que soluciones ad hoc. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.security_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_mfa

## Question 8
**Concept:** Salesforce as an Identity Provider (17%)

**Question (EN):** Northern Trail Outfitters manages application functional permissions centrally as Active Directory groups. The CRM_SuperUser and CRM_Reporting_SuperUser groups should respectively give the user the SuperUser and Reporting_SuperUser permission set in Salesforce, Salesforce is the service provider to a Security Assertion Markup Language (SAML) identity provider, How should an identity architect ensure the Active Directory groups are reflected correctly when a user accesses Salesforce?

**Correct Answer:** D

**Detailed Explanation (ES):**
La respuesta correcta es **D** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. Cuando Salesforce actua como IdP, la decision correcta normalmente depende del protocolo requerido por el SP y del tipo de token/assertion que necesita la aplicacion consumidora. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.sso_provider_enable.htm&type=5
- https://help.salesforce.com/s/articleView?id=sf.sso_saml.htm&type=5

## Question 9
**Concept:** Community (Partner and Customer) (18%)

**Question (EN):** An identity architect has been asked to recommend a solution that allows administrators to configure personalized alert messages to users before they land on the Experience Cloud site (formerly known as Community) homepage. What is recommended to fulfill this requirement with the least amount of customization? © Use Login Flows to add a screen that shows personalized alerts.

**Correct Answer:** A

**Detailed Explanation (ES):**
La respuesta correcta es **A** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. En Experience Cloud la clave es alinear login, registro y experiencia de usuario con capacidades nativas como Login Discovery, self-registration controlada y branding dinamico. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.networks_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_external

## Question 10
**Concept:** Community (Partner and Customer) (18%)

**Question (EN):** An Identity and Access Management (IAM) architect is tasked with unifying multiple B2C Commerce sites and an Experience Cloud community What should the IAM Architect do to fulfill this requirement? 8. © Configure community as a Security Assertion Markup Language (SAML) identity provider and enable Just-in-Time Provisioning to B2C Commerce.

**Correct Answer:** D

**Detailed Explanation (ES):**
La respuesta correcta es **D** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. En Experience Cloud la clave es alinear login, registro y experiencia de usuario con capacidades nativas como Login Discovery, self-registration controlada y branding dinamico. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.networks_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_external

## Question 11
**Concept:** Community (Partner and Customer) (18%)

**Question (EN):** Northern Trail Outfitters (NTO) wants its customers to use phone numbers to log in to their new digital portal, which was designed and built using Salesforce Experience Cloud. In order to access the portal, the user will need to do the following: 1. Enter a phone number and/or email address 2. Enter a verification code that is to be sent via email or text. What is the recommended approach to fulfill this requirement?

**Correct Answer:** B

**Detailed Explanation (ES):**
La respuesta correcta es **B** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. En Experience Cloud la clave es alinear login, registro y experiencia de usuario con capacidades nativas como Login Discovery, self-registration controlada y branding dinamico. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.networks_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_external

## Question 12
**Concept:** Accepting Third-Party Identity in Salesforce (21%)

**Question (EN):** as Security Assertion Markup Language (SAML) or OAuth. NTO wants to use Salesforce Identity to register and authenticate new customers on the website. Which three Salesforce features should an Identity architect use in order to provide social sign-in capabilities for the website? Delegated Authentication

**Correct Answer:** A

**Detailed Explanation (ES):**
La respuesta correcta es **A** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. En este dominio suele primar la federacion estandar (SAML/OAuth/OIDC), el aprovisionamiento correcto y la minimizacion de logica custom cuando existe una capacidad nativa de plataforma. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.identity_provider_intro.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_login

## Question 13
**Concept:** Access Management Best Practices (15%)

**Question (EN):** An identity architect is implementing a mobile-first Consumer Identity Access Management (CIAM) for external users. User authentication is the only requirement. The users email or mobile phone number should Which two licenses are needed to meet this requirement? SMS Verification Credits

**Correct Answer:** A

**Detailed Explanation (ES):**
La respuesta correcta es **A** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. Desde buenas practicas de acceso, se prioriza reducir superficie de riesgo, mantener trazabilidad de autenticacion y aplicar controles estandar antes que soluciones ad hoc. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.security_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_mfa

## Question 14
**Concept:** Community (Partner and Customer) (18%)

**Question (EN):** Universal Container’s (UC) is using Salesforce Experience Cloud site for its container wholesale business. The Identity architect wants to use an authentication provider for the new site. Which two options should be utilized in creating an authentication provider?

**Correct Answer:** AB

**Detailed Explanation (ES):**
La respuesta correcta es **AB** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. Esta pregunta exige seleccionar exactamente **2** opciones; la combinacion propuesta respeta esa cardinalidad y evita sobreseleccion o subseleccion. En Experience Cloud la clave es alinear login, registro y experiencia de usuario con capacidades nativas como Login Discovery, self-registration controlada y branding dinamico. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.networks_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_external

## Question 15
**Concept:** Access Management Best Practices (15%)

**Question (EN):** Users logging into Salesforce are frequently prompted to verify their identity. The identity architect is required to provide recommendations so that frequency of prompt verification can be reduced. What should the identity architect recommend to meet the requirement?

**Correct Answer:** D

**Detailed Explanation (ES):**
La respuesta correcta es **D** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. Desde buenas practicas de acceso, se prioriza reducir superficie de riesgo, mantener trazabilidad de autenticacion y aplicar controles estandar antes que soluciones ad hoc. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.security_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_mfa

## Question 16
**Concept:** Identity Management Concepts (17%)

**Question (EN):** An identity professional, responsible for ensuring secure access to the Salesforce platform, needs to audit and verify user activity during and after login. They want to monitor login attempts, track user authentication methods, and identify suspicious behavior or unauthorized access. Which tool or feature should they leverage to achieve this objective?

**Correct Answer:** C

**Detailed Explanation (ES):**
La respuesta correcta es **C** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. A nivel de conceptos de gestion de identidad, la opcion correcta suele ser la que respeta el flujo estandar de autenticacion/autorizacion y el principio de minimo privilegio. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.identity_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_basics

## Question 17
**Concept:** Salesforce as an Identity Provider (17%)

**Question (EN):** Northern Trail Outfitters (NTO) uses a Security Assertion Markup Language (SAML)-based Identity Provider (IdP) to authenticate employees to all systems. The IdP authenticates users against a Lightweight Directory Access Protocol (LDAP) directory and has access to user information. NTO wants to minimize Salesforce license usage since only a small percentage of users need Salesforce. What is recommended to ensure new employees have immediate access to Salesforce using their current IdP?

**Correct Answer:** C

**Detailed Explanation (ES):**
La respuesta correcta es **C** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. Cuando Salesforce actua como IdP, la decision correcta normalmente depende del protocolo requerido por el SP y del tipo de token/assertion que necesita la aplicacion consumidora. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.sso_provider_enable.htm&type=5
- https://help.salesforce.com/s/articleView?id=sf.sso_saml.htm&type=5

## Question 18
**Concept:** Community (Partner and Customer) (18%)

**Question (EN):** Northern Trail Outfitters (NTO) wants its customers to use phone numbers to log in to their new digital portal, which was designed and built using Salesforce Experience Cloud. In order to access the portal, the user will need to do the following: 1. Enter a phone number and/or email address 2. Enter a verification code that is to be sent via email or text. What is the recommended approach to fulfill this requirement?

**Correct Answer:** B

**Detailed Explanation (ES):**
La respuesta correcta es **B** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. En Experience Cloud la clave es alinear login, registro y experiencia de usuario con capacidades nativas como Login Discovery, self-registration controlada y branding dinamico. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.networks_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_external

## Question 19
**Concept:** Accepting Third-Party Identity in Salesforce (21%)

**Question (EN):** Universal Containers is creating 2 mobile application that will be secured by Salesforce Identity using the OAuth 2.0 user-agent flow. Application users will authenticate using username and password. They should not be forced to approve API access in the mobile app or reauthenticate for 3 months. Which two connected ape ontions nnd tm he rankimorad = fulfil this Use case?

**Correct Answer:** AB

**Detailed Explanation (ES):**
La respuesta correcta es **AB** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. Esta pregunta exige seleccionar exactamente **2** opciones; la combinacion propuesta respeta esa cardinalidad y evita sobreseleccion o subseleccion. En este dominio suele primar la federacion estandar (SAML/OAuth/OIDC), el aprovisionamiento correcto y la minimizacion de logica custom cuando existe una capacidad nativa de plataforma. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.identity_provider_intro.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_login

## Question 20
**Concept:** Salesforce as an Identity Provider (17%)

**Question (EN):** Northern Trail Outfitters manages application functional permissions centrally as Active Directory groups. The CRM_SuperUser and CRM_Reporting_SuperUser groups should respectively give the user the SuperUser and Reporting_SuperUser permission set in Salesforce. Salesforce is the service provider to a Security Assertion Markup Language (SAML) identity provider. How should an identity architect ensure the Active Directory groups are reflected correctly when a user accesses Salesforce?

**Correct Answer:** BC

**Detailed Explanation (ES):**
La respuesta correcta es **BC** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. Esta pregunta exige seleccionar exactamente **2** opciones; la combinacion propuesta respeta esa cardinalidad y evita sobreseleccion o subseleccion. Cuando Salesforce actua como IdP, la decision correcta normalmente depende del protocolo requerido por el SP y del tipo de token/assertion que necesita la aplicacion consumidora. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.sso_provider_enable.htm&type=5
- https://help.salesforce.com/s/articleView?id=sf.sso_saml.htm&type=5

## Question 21
**Concept:** Salesforce Identity (12%)

**Question (EN):** Universal Containers (UC) wants to provide single sign-on (SSO) for a business-to-consumer (B2C) application using Salesforce Identity. Which Salesforce license should UC utilize to implement this use case?

**Correct Answer:** D

**Detailed Explanation (ES):**
La respuesta correcta es **D** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. En Salesforce Identity se evalua especialmente licenciamiento, capacidades de SSO y patrones de autenticacion compatibles con el caso de uso empresarial. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.identity_main.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_login

## Question 22
**Concept:** Accepting Third-Party Identity in Salesforce (21%)

**Question (EN):** Universal Containers is creating a web application that will be secured by Salesforce Identity using the OAuth 2.0 Web Server Flow (this flow uses the OAuth 2.0 authorization code grant type). Which three OAuth concepts apply to this flow?

**Correct Answer:** A

**Detailed Explanation (ES):**
La respuesta correcta es **A** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. En este dominio suele primar la federacion estandar (SAML/OAuth/OIDC), el aprovisionamiento correcto y la minimizacion de logica custom cuando existe una capacidad nativa de plataforma. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.identity_provider_intro.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_login

## Question 23
**Concept:** Identity Management Concepts (17%)

**Question (EN):** An insurance company has a connected app in its Salesforce environment that is used to integrate with a Google Workspace (formerly known as G Suite). ‘An identity and access management (IAM) architect has been asked to implement automation to enable users, freeze/suspend users, disable users, and reactivate existing users in Google Workspace upon similar actions in Salesforcs Which solution is recommended to meet this requirement?

**Correct Answer:** A

**Detailed Explanation (ES):**
La respuesta correcta es **A** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. A nivel de conceptos de gestion de identidad, la opcion correcta suele ser la que respeta el flujo estandar de autenticacion/autorizacion y el principio de minimo privilegio. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.identity_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_basics

## Question 24
**Concept:** Accepting Third-Party Identity in Salesforce (21%)

**Question (EN):** Universal Containers is designing an identity architecture that involves integrating Salesforce with an external directory service. The external directory service will act as the central repository for user authentication and authorization across multiple systems within the organization. Which approach should be evaluated to establish trust between Salesforce and the external directory service? © Implementing a federated identity solution based on SAML (Security Assertion Markup Language).

**Correct Answer:** B

**Detailed Explanation (ES):**
La respuesta correcta es **B** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. En este dominio suele primar la federacion estandar (SAML/OAuth/OIDC), el aprovisionamiento correcto y la minimizacion de logica custom cuando existe una capacidad nativa de plataforma. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.identity_provider_intro.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_login

## Question 25
**Concept:** Identity Management Concepts (17%)

**Question (EN):** Universal Containers (UC) is rolling out its new Customer Identity and Access Management Solution built on top of its existing Salesforce instance. UC wants to allow customers to login using Facebook, Google, and other social sign-on providers. How should this functionality be enabled for UC, assuming all social

**Correct Answer:** B

**Detailed Explanation (ES):**
La respuesta correcta es **B** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. A nivel de conceptos de gestion de identidad, la opcion correcta suele ser la que respeta el flujo estandar de autenticacion/autorizacion y el principio de minimo privilegio. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.identity_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_basics

## Question 26
**Concept:** Community (Partner and Customer) (18%)

**Question (EN):** Northern Trail Outfitters would like to use a portal built on Salesforce Experience Cloud for customer self-service. Guests of the portal should be able to self-register, but be unable to automatically be assigned to a contact record until verified. External Identity licenses have been purchased for the project. After registered guests complete an onboarding process, a flow will create the appropriate account and contact records for the user. Which three steps should an identity architect follow to implement the outlined requirements? AG) Customize the self-registration Apex handler to create only the user record. 8. ‘Select the "Configurable Self-Reg Page” option under Login & Registration.

**Correct Answer:** B

**Detailed Explanation (ES):**
La respuesta correcta es **B** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. En Experience Cloud la clave es alinear login, registro y experiencia de usuario con capacidades nativas como Login Discovery, self-registration controlada y branding dinamico. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.networks_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_external

## Question 27
**Concept:** Salesforce as an Identity Provider (17%)

**Question (EN):** An identity architect's client has a homegrown identity provider (IdP). Salesforce is used as the service provider (SP). The head of IT is worried that during a SP initiated single sign-on (SSO), the Security Assertion Markup Language (SAML) request content will be altered. What should the identity architect recommend to make sure that there is additional trust between the SP and the IdP? Ay Encrypt the SAML Request using certification authority (CA) signed certificate and decrypt on IdP.

**Correct Answer:** C

**Detailed Explanation (ES):**
La respuesta correcta es **C** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. Cuando Salesforce actua como IdP, la decision correcta normalmente depende del protocolo requerido por el SP y del tipo de token/assertion que necesita la aplicacion consumidora. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.sso_provider_enable.htm&type=5
- https://help.salesforce.com/s/articleView?id=sf.sso_saml.htm&type=5

## Question 28
**Concept:** Accepting Third-Party Identity in Salesforce (21%)

**Question (EN):** Northern Trail Outfitters (NTO) leverages Microsoft Active Directory (AD) for management of employee usernames, passwords, permissions, and asset access. NTO also owns a third-party single sign-on (SSO) solution. The third-party party SSO solution is used for all corporate applications, including Salesforce. NTO has asked an architect to explore Salesforce Identity Connect for automatic provisioning and deprovisioning of users in Salesforce. What role does identity Connect play in the outlined requirements?

**Correct Answer:** BD

**Detailed Explanation (ES):**
La respuesta correcta es **BD** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. Esta pregunta exige seleccionar exactamente **2** opciones; la combinacion propuesta respeta esa cardinalidad y evita sobreseleccion o subseleccion. En este dominio suele primar la federacion estandar (SAML/OAuth/OIDC), el aprovisionamiento correcto y la minimizacion de logica custom cuando existe una capacidad nativa de plataforma. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.identity_provider_intro.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_login

## Question 29
**Concept:** Community (Partner and Customer) (18%)

**Question (EN):** Universal Containers is implementing a new Experience Cloud site and the identity architect wants to use dynamic branding features as part of the login process.

**Correct Answer:** BC

**Detailed Explanation (ES):**
La respuesta correcta es **BC** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. Esta pregunta exige seleccionar exactamente **2** opciones; la combinacion propuesta respeta esa cardinalidad y evita sobreseleccion o subseleccion. En Experience Cloud la clave es alinear login, registro y experiencia de usuario con capacidades nativas como Login Discovery, self-registration controlada y branding dinamico. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.networks_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_external

## Question 30
**Concept:** Community (Partner and Customer) (18%)

**Question (EN):** Northern Trail Outfitters (NTO) uses the Customer 360 Platform implemented on Salesforce Experience Cloud. The development team in charge has learned of a contactless user feature, which can reduce the overhead of managing customers and partners by creating users without contact information. What is the potential impact to the architecture if NTO decides to implement this feature?

**Correct Answer:** C

**Detailed Explanation (ES):**
La respuesta correcta es **C** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. En Experience Cloud la clave es alinear login, registro y experiencia de usuario con capacidades nativas como Login Discovery, self-registration controlada y branding dinamico. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.networks_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_external

## Question 31
**Concept:** Salesforce as an Identity Provider (17%)

**Question (EN):** Northern Trail Outfitters (NTO) uses a Security Assertion Markup Language (SAML)-based Identity Provider (IdP) to authenticate employees to all systems. The IdP authenticates users against a Lightweight Directory Access Protocol (LDAP) directory and has access to user information. NTO wants to minimize Salesforce license usage since only a small percentage of users need Salesforce. What is recommended to ensure new employees have immediate access to Salesforce using their current IdP?

**Correct Answer:** D

**Detailed Explanation (ES):**
La respuesta correcta es **D** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. Cuando Salesforce actua como IdP, la decision correcta normalmente depende del protocolo requerido por el SP y del tipo de token/assertion que necesita la aplicacion consumidora. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.sso_provider_enable.htm&type=5
- https://help.salesforce.com/s/articleView?id=sf.sso_saml.htm&type=5

## Question 32
**Concept:** Identity Management Concepts (17%)

**Question (EN):** An administrator created a connected app for a custom web application in Salesforce which needs to be visible as a tile In App Launcher. The tile for the custom web application is missing in the app launcher for all users in Salesforce, The administrator requested assistance from an identity architect to resolve the issue. Which two reasons are the source of the Issue?

**Correct Answer:** CD

**Detailed Explanation (ES):**
La respuesta correcta es **CD** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. Esta pregunta exige seleccionar exactamente **2** opciones; la combinacion propuesta respeta esa cardinalidad y evita sobreseleccion o subseleccion. A nivel de conceptos de gestion de identidad, la opcion correcta suele ser la que respeta el flujo estandar de autenticacion/autorizacion y el principio de minimo privilegio. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.identity_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_basics

## Question 33
**Concept:** Accepting Third-Party Identity in Salesforce (21%)

**Question (EN):** An identity architect is setting up an integration between Salesforce and a third-party system. The third-party system needs to be able to authenticate to Salesforce and then make API calls against the REST API. One of the requirements is that the solution needs to ensure the third party service providers connected app in Salesforce minimizes the need for end user interaction and maximizes security. Which OAuth flow should be used to fulfill the requirement?

**Correct Answer:** A

**Detailed Explanation (ES):**
La respuesta correcta es **A** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. En este dominio suele primar la federacion estandar (SAML/OAuth/OIDC), el aprovisionamiento correcto y la minimizacion de logica custom cuando existe una capacidad nativa de plataforma. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.identity_provider_intro.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_login

## Question 34
**Concept:** Community (Partner and Customer) (18%)

**Question (EN):** Universal Containers (UC) has decided to replace the homegrown customer portal with Salesforce Experience Cloud. UC will continue to use its third-party single sign-on (SSO) solution that stores all of its customer and partner credentials. The first time a customer logs in to the Experience Cloud site through SSO, a user record needs to be created automatically. Which solution should an identity architect recommend in order to automatically provision users in Salesforce upon login?

**Correct Answer:** C

**Detailed Explanation (ES):**
La respuesta correcta es **C** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. En Experience Cloud la clave es alinear login, registro y experiencia de usuario con capacidades nativas como Login Discovery, self-registration controlada y branding dinamico. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.networks_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_external

## Question 35
**Concept:** Identity Management Concepts (17%)

**Question (EN):** Universal Containers (UC) is considering a Customer 360 initiative to gain a single source of the truth for its customer data across disparate systems and services. UC wants to understand the primary benefits of Customer 360 Identity and how it contributes to a successful Customer 360 Truth project. What are two are key benefits of Customer 360 Identity as it relates to Customer 360?

**Correct Answer:** C

**Detailed Explanation (ES):**
La respuesta correcta es **C** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. A nivel de conceptos de gestion de identidad, la opcion correcta suele ser la que respeta el flujo estandar de autenticacion/autorizacion y el principio de minimo privilegio. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.identity_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_basics

## Question 36
**Concept:** Community (Partner and Customer) (18%)

**Question (EN):** Northern Trail Outfitters (NTO) is launching a new sportswear brand on its existing consumer portal built on Salesforce Experience Cloud. As part of the launch, emails with promotional links will be sent to existing customers to log in and claim a discount. The marketing manager would like the portal dynamically branded so that users will be directed to the brand link they clicked on; otherwise, users will view a recognizable NTO-branded page. The campaign is launching quickly, so there is no time to procure any additional licenses. However, the development team is available to apply any required changes to the portal. Which approach should the identity architect recommend?

**Correct Answer:** A

**Detailed Explanation (ES):**
La respuesta correcta es **A** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. En Experience Cloud la clave es alinear login, registro y experiencia de usuario con capacidades nativas como Login Discovery, self-registration controlada y branding dinamico. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.networks_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_external

## Question 37
**Concept:** Community (Partner and Customer) (18%)

**Question (EN):** An identity professional is working on the configuration of a connected app for Universal Container's (UC) partner portal. UC wants to allow external users to access certain Salesforce data and perform limited actions. However, they also want to enforce additional security measures, such as IP restrictions and session timeout settings. Which configuration option should be used to enforce IP restrictions and session timeout settings for the connected app? Session Settings £.O Login IP Ranges €.Q Custom Permissions

**Correct Answer:** AC

**Detailed Explanation (ES):**
La respuesta correcta es **AC** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. Esta pregunta exige seleccionar exactamente **2** opciones; la combinacion propuesta respeta esa cardinalidad y evita sobreseleccion o subseleccion. En Experience Cloud la clave es alinear login, registro y experiencia de usuario con capacidades nativas como Login Discovery, self-registration controlada y branding dinamico. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.networks_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_external

## Question 38
**Concept:** Accepting Third-Party Identity in Salesforce (21%)

**Question (EN):** Universal Containers is creating a mobile application that will be secured by Salesforce Identity using the OAuth 2.0 user-agent flow (this flow uses the OAuth 2.0 implicit grant type). Which three OAuth concepts apply to this flow?

**Correct Answer:** B

**Detailed Explanation (ES):**
La respuesta correcta es **B** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. En este dominio suele primar la federacion estandar (SAML/OAuth/OIDC), el aprovisionamiento correcto y la minimizacion de logica custom cuando existe una capacidad nativa de plataforma. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.identity_provider_intro.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_login

## Question 39
**Concept:** Identity Management Concepts (17%)

**Question (EN):** User authentication ‘ ———_ ee -

**Correct Answer:** AB

**Detailed Explanation (ES):**
La respuesta correcta es **AB** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. Esta pregunta exige seleccionar exactamente **2** opciones; la combinacion propuesta respeta esa cardinalidad y evita sobreseleccion o subseleccion. A nivel de conceptos de gestion de identidad, la opcion correcta suele ser la que respeta el flujo estandar de autenticacion/autorizacion y el principio de minimo privilegio. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.identity_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_basics

## Question 40
**Concept:** Salesforce as an Identity Provider (17%)

**Question (EN):** Universal Containers (UC) currently uses Salesforce Sales Cloud and an external billing application. Both Salesforce and the billing application are accessed several times a day to manage customers. UC would like to configure single sign-on and leverage Salesforce as the identity provider. Additionally, UC would like the billing application to be accessible from Salesforce. A redirect is acceptable. Which two Salesforce tools should an identity architect recommend to satisfy the requirements? 4@ Salesforce Canvas 8. @@ App Launcher €.( Identity Connect

**Correct Answer:** BC

**Detailed Explanation (ES):**
La respuesta correcta es **BC** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. Esta pregunta exige seleccionar exactamente **2** opciones; la combinacion propuesta respeta esa cardinalidad y evita sobreseleccion o subseleccion. Cuando Salesforce actua como IdP, la decision correcta normalmente depende del protocolo requerido por el SP y del tipo de token/assertion que necesita la aplicacion consumidora. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.sso_provider_enable.htm&type=5
- https://help.salesforce.com/s/articleView?id=sf.sso_saml.htm&type=5

## Question 41
**Concept:** Community (Partner and Customer) (18%)

**Question (EN):** Northern Trail Outfitters (NT‘ sportswear brand on its existing consur) js launching a new Experience Cloud. As part of the launclner portal built on Salesforce will be sent to existing customers to log, emails with promotional links marketing manager would like the port, jn and claim a discount. The users will be directed to the brand link a] dynamically branded so that users will view a recognizable NTO-bratthey clicked on; otherwise, aided page. The campaign is launching quickly, so t additional licenses. However, the develthere is no time to procure any apply any required changes to the port;pment team is available to al. Which approach should the identity arc . hitect recommend?

**Correct Answer:** C

**Detailed Explanation (ES):**
La respuesta correcta es **C** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. En Experience Cloud la clave es alinear login, registro y experiencia de usuario con capacidades nativas como Login Discovery, self-registration controlada y branding dinamico. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.networks_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_external

## Question 42
**Concept:** Identity Management Concepts (17%)

**Question (EN):** Which two things should be done to ensure end users can only use single sign-on (SSO) to login in to Salesforce? Enable My Domain and select "Prevent login from https://login.salesforce.com".

**Correct Answer:** D

**Detailed Explanation (ES):**
La respuesta correcta es **D** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. A nivel de conceptos de gestion de identidad, la opcion correcta suele ser la que respeta el flujo estandar de autenticacion/autorizacion y el principio de minimo privilegio. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.identity_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_basics

## Question 43
**Concept:** Identity Management Concepts (17%)

**Question (EN):** [Texto OCR degradado]

**Correct Answer:** D

**Detailed Explanation (ES):**
La respuesta correcta es **D** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. A nivel de conceptos de gestion de identidad, la opcion correcta suele ser la que respeta el flujo estandar de autenticacion/autorizacion y el principio de minimo privilegio. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.identity_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_basics

## Question 44
**Concept:** Access Management Best Practices (15%)

**Question (EN):** Northern Trail Outfitters (NTO) is planning to build a new customer service portal and wants to use passwordless login, allowing customers to login with a one-time passcode sent to them via email or SMS. How should the quantity of required Identity Verification Credits be estimated?

**Correct Answer:** D

**Detailed Explanation (ES):**
La respuesta correcta es **D** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. Desde buenas practicas de acceso, se prioriza reducir superficie de riesgo, mantener trazabilidad de autenticacion y aplicar controles estandar antes que soluciones ad hoc. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.security_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_mfa

## Question 45
**Concept:** Community (Partner and Customer) (18%)

**Question (EN):** Universal Containers (UC) has decided to replace the homegrown customer portal with Salesforce Experience Cloud. UC will continue to use its third-party single sign-on (SSO) solution that stores all of its customer and partner credentials. The first time a customer logs in to the Experience Cloud site through SSO, a user record needs to be created automatically. Which solution should an identity architect recommend in order to automatically provision users in Salesforce upon login?

**Correct Answer:** A

**Detailed Explanation (ES):**
La respuesta correcta es **A** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. En Experience Cloud la clave es alinear login, registro y experiencia de usuario con capacidades nativas como Login Discovery, self-registration controlada y branding dinamico. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.networks_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_external

## Question 46
**Concept:** Salesforce as an Identity Provider (17%)

**Question (EN):** Markup Language (SAML) and OpenID Connect (OIDC). When Salesforce is acting as Identity Provider for this SP, which use case is the determining factor when choosing OIDC or SAML? © The SP needs to perform API calis back to Salesforce on behalf of the user after the user logs in to the service provider. 6. oO OIDC is more secure than SAML and therefore is the obvious choice.

**Correct Answer:** A

**Detailed Explanation (ES):**
La respuesta correcta es **A** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. Cuando Salesforce actua como IdP, la decision correcta normalmente depende del protocolo requerido por el SP y del tipo de token/assertion que necesita la aplicacion consumidora. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.sso_provider_enable.htm&type=5
- https://help.salesforce.com/s/articleView?id=sf.sso_saml.htm&type=5

## Question 47
**Concept:** Community (Partner and Customer) (18%)

**Question (EN):** Northern Trail Outfitters would lke to use a porta bult on Salesforce Experience Cloul for customer self-service. Guests of the portal should be able to self-register, but be unable to automatically be assigned to a contact record until verted. External Identity licenses have been purchased forthe project, ‘ter registered quests complete an onboarding process, a flow wil create the appropriate account and contact records forthe user: Which three steos should an identity architect follow to implement the outlined requirements?

**Correct Answer:** B

**Detailed Explanation (ES):**
La respuesta correcta es **B** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. En Experience Cloud la clave es alinear login, registro y experiencia de usuario con capacidades nativas como Login Discovery, self-registration controlada y branding dinamico. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.networks_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_external

## Question 48
**Concept:** Salesforce Identity (12%)

**Question (EN):** Universal Containers (UC) wants to provide single sign-on (SSO) for a business-to-consumer (B2C) application using Salesforce Identity. Which Salesforce license should UC utilize to implement this use case?

**Correct Answer:** B

**Detailed Explanation (ES):**
La respuesta correcta es **B** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. En Salesforce Identity se evalua especialmente licenciamiento, capacidades de SSO y patrones de autenticacion compatibles con el caso de uso empresarial. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.identity_main.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_login

## Question 49
**Concept:** Community (Partner and Customer) (18%)

**Question (EN):** The CMO of an advertising company has invited an Identity and Access Management (IAM) specialist to discuss Salesforce out-of-box capabilities for configuring the company’s login and registration experience on Salesforce Experience Cloud. The CMO is looking to brand the login page with the company's logo, background color, login button color, and dynamic right-frame from an external URL. Which two solutions should the IAM specialist recommend? Login & Registration pages can be branded In the Community Administration settings.

**Correct Answer:** AC

**Detailed Explanation (ES):**
La respuesta correcta es **AC** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. Esta pregunta exige seleccionar exactamente **2** opciones; la combinacion propuesta respeta esa cardinalidad y evita sobreseleccion o subseleccion. En Experience Cloud la clave es alinear login, registro y experiencia de usuario con capacidades nativas como Login Discovery, self-registration controlada y branding dinamico. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.networks_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_external

## Question 50
**Concept:** Identity Management Concepts (17%)

**Question (EN):** [Texto OCR degradado]

**Correct Answer:** A

**Detailed Explanation (ES):**
La respuesta correcta es **A** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. A nivel de conceptos de gestion de identidad, la opcion correcta suele ser la que respeta el flujo estandar de autenticacion/autorizacion y el principio de minimo privilegio. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.identity_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_basics

## Question 51
**Concept:** Community (Partner and Customer) (18%)

**Question (EN):** Northern Trail Outfitters (NTO) uses the Customer 360 Platform implemented on Salesforce Experience Cloud. The development team in charge has learned of a contactless user feature, which can reduce the overhead of managing customers and partners by creating users without contact information. What is the potential impact to the architecture if NTO decides to implement this feature?

**Correct Answer:** C

**Detailed Explanation (ES):**
La respuesta correcta es **C** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. En Experience Cloud la clave es alinear login, registro y experiencia de usuario con capacidades nativas como Login Discovery, self-registration controlada y branding dinamico. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.networks_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_external

## Question 52
**Concept:** Accepting Third-Party Identity in Salesforce (21%)

**Question (EN):** Universal Containers is creating a mobile application that will be secured by Salesforce Identity using the OAuth 2.0 user-agent flow (this flow uses the OAuth 2.0 Implicit grant type). Which three OAuth concepts apply to this flow? Scopes Client ID Authorization Code Verification Code Refresh Token Salesforce Certified Identity and Access Management Archit«

**Correct Answer:** A

**Detailed Explanation (ES):**
La respuesta correcta es **A** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. En este dominio suele primar la federacion estandar (SAML/OAuth/OIDC), el aprovisionamiento correcto y la minimizacion de logica custom cuando existe una capacidad nativa de plataforma. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.identity_provider_intro.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_login

## Question 53
**Concept:** Salesforce as an Identity Provider (17%)

**Question (EN):** Universal Containers uses Salesforce as an identity provider and Concur as the Employee Expense management system. The HR director wants to ensure Concur accounts for employees are created only after the appropriate approval in the Salesforce org, men hee steps shuld heey whee =o mement rs eaarement? ‘AG@ robe User Provstonin fo the comers app. 8.) Create an approval process fora custom objet asocoted wth the provsoring flow, ©) create an approval proces for User object associated wth the provisoing fw. ©. €@ Create an approval process for UserProvsoningResuest object assacied withthe provstoin on ‘

**Correct Answer:** CE

**Detailed Explanation (ES):**
La respuesta correcta es **CE** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. Esta pregunta exige seleccionar exactamente **2** opciones; la combinacion propuesta respeta esa cardinalidad y evita sobreseleccion o subseleccion. Cuando Salesforce actua como IdP, la decision correcta normalmente depende del protocolo requerido por el SP y del tipo de token/assertion que necesita la aplicacion consumidora. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.sso_provider_enable.htm&type=5
- https://help.salesforce.com/s/articleView?id=sf.sso_saml.htm&type=5

## Question 54
**Concept:** Identity Management Concepts (17%)

**Question (EN):** The CMO for cc Manag f-box capabilities t-frame from an external URL ‘h two solutions should the IAM Choo: 2 answers Press the "Prnt Scrn” on vour kevboard to take a asta Sueeui “Gan eau

**Correct Answer:** AB

**Detailed Explanation (ES):**
La respuesta correcta es **AB** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. Esta pregunta exige seleccionar exactamente **2** opciones; la combinacion propuesta respeta esa cardinalidad y evita sobreseleccion o subseleccion. A nivel de conceptos de gestion de identidad, la opcion correcta suele ser la que respeta el flujo estandar de autenticacion/autorizacion y el principio de minimo privilegio. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.identity_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_basics

## Question 55
**Concept:** Community (Partner and Customer) (18%)

**Question (EN):** Universal Containers wants to allow its customers to log in to its Experience Cloud via a third party authentication provider that What should an identity architect do to fulfill this requirement?

**Correct Answer:** D

**Detailed Explanation (ES):**
La respuesta correcta es **D** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. En Experience Cloud la clave es alinear login, registro y experiencia de usuario con capacidades nativas como Login Discovery, self-registration controlada y branding dinamico. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.networks_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_external

## Question 56
**Concept:** Identity Management Concepts (17%)

**Question (EN):** Northern Trail Outfitters (NTO) wants to give customers the ability to submit and manage issues with their purchases. It is important for NTO to give its customers the ability to login with their Facebook and Twitter credentials. What should an identity architect recommend to meet these requirements?

**Correct Answer:** D

**Detailed Explanation (ES):**
La respuesta correcta es **D** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. A nivel de conceptos de gestion de identidad, la opcion correcta suele ser la que respeta el flujo estandar de autenticacion/autorizacion y el principio de minimo privilegio. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.identity_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_basics

## Question 57
**Concept:** Salesforce as an Identity Provider (17%)

**Question (EN):** An identity architect's client has a homegrown identity provider (IdP). Salesforce is used as the service provider (SP). The head of IT is worried that during a SP initiated single sign-on (SSO), the Security Assertion Markup Language (SAML) request content will be altered. What should the identity architect recommend to make sure that there is additional trust between the SP and the IdP?

**Correct Answer:** C

**Detailed Explanation (ES):**
La respuesta correcta es **C** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. Cuando Salesforce actua como IdP, la decision correcta normalmente depende del protocolo requerido por el SP y del tipo de token/assertion que necesita la aplicacion consumidora. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.sso_provider_enable.htm&type=5
- https://help.salesforce.com/s/articleView?id=sf.sso_saml.htm&type=5

## Question 58
**Concept:** Salesforce as an Identity Provider (17%)

**Question (EN):** Northern Trail Outfitters manages application functional permissions centrally as Active Directory groups. The CRM_SuperUse and CRM _ Reporting SuperUser groups should respectively give the user the SuperUser and Reporting_SuperUser permission set in Salesforce. Salesforce is the service provider to a Security Assertion Markup Language (SAML) identity provider. How should an identity architect ensure the Active Directory groups are reflected correctly when a user accesses Salesforce?

**Correct Answer:** B

**Detailed Explanation (ES):**
La respuesta correcta es **B** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. Cuando Salesforce actua como IdP, la decision correcta normalmente depende del protocolo requerido por el SP y del tipo de token/assertion que necesita la aplicacion consumidora. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.sso_provider_enable.htm&type=5
- https://help.salesforce.com/s/articleView?id=sf.sso_saml.htm&type=5

## Question 59
**Concept:** Identity Management Concepts (17%)

**Question (EN):** [Texto OCR degradado]

**Correct Answer:** C

**Detailed Explanation (ES):**
La respuesta correcta es **C** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. A nivel de conceptos de gestion de identidad, la opcion correcta suele ser la que respeta el flujo estandar de autenticacion/autorizacion y el principio de minimo privilegio. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.identity_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_basics

## Question 60
**Concept:** Salesforce as an Identity Provider (17%)

**Question (EN):** Universal Containers (UC) currently uses Salesforce Sales Cloud and an external bling application. Both Salesforce and the billing application are accessed several times a day to manage customers. UC would like to configure single sign-on and leverage Salesforce as the identity provider. ditionally, UC would like the biling application to be accessible from Salesforce. A redirect is acceptable. Which twa Salnetoren rants chavid an dante architect recommend to satisty the requirements?

**Correct Answer:** C

**Detailed Explanation (ES):**
La respuesta correcta es **C** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. Cuando Salesforce actua como IdP, la decision correcta normalmente depende del protocolo requerido por el SP y del tipo de token/assertion que necesita la aplicacion consumidora. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.sso_provider_enable.htm&type=5
- https://help.salesforce.com/s/articleView?id=sf.sso_saml.htm&type=5

## Question 61
**Concept:** Accepting Third-Party Identity in Salesforce (21%)

**Question (EN):** Universal Containers is creating a mobile application that will be secured by Salesforce Identity using the OAuth 2.0 user-agent flow. Application users will authenticate using username and password. They should not be forced to approve API access in the mobile app or reauthenticate for 3 months. Which two connected app options need to be configured to fulfill this use case?

**Correct Answer:** B

**Detailed Explanation (ES):**
La respuesta correcta es **B** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. En este dominio suele primar la federacion estandar (SAML/OAuth/OIDC), el aprovisionamiento correcto y la minimizacion de logica custom cuando existe una capacidad nativa de plataforma. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.identity_provider_intro.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_login

## Question 62
**Concept:** Salesforce Identity (12%)

**Question (EN):** Universal Containers (UC) has built a custom time tracking app for its employees on a third party system. UC wants to leverage Salesforce Identity to control access to the custom app. requirement?

**Correct Answer:** B

**Detailed Explanation (ES):**
La respuesta correcta es **B** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. En Salesforce Identity se evalua especialmente licenciamiento, capacidades de SSO y patrones de autenticacion compatibles con el caso de uso empresarial. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.identity_main.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_login

## Question 63
**Concept:** Identity Management Concepts (17%)

**Question (EN):** << Ga = Users

**Correct Answer:** A

**Detailed Explanation (ES):**
La respuesta correcta es **A** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. A nivel de conceptos de gestion de identidad, la opcion correcta suele ser la que respeta el flujo estandar de autenticacion/autorizacion y el principio de minimo privilegio. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.identity_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_basics

## Question 64
**Concept:** Accepting Third-Party Identity in Salesforce (21%)

**Question (EN):** ADFS Americas

**Correct Answer:** A

**Detailed Explanation (ES):**
La respuesta correcta es **A** porque es la opcion que mejor cumple el requisito funcional y de seguridad planteado en el escenario. En este dominio suele primar la federacion estandar (SAML/OAuth/OIDC), el aprovisionamiento correcto y la minimizacion de logica custom cuando existe una capacidad nativa de plataforma. Las alternativas descartadas normalmente fallan por no ajustarse al protocolo, por requerir personalizacion innecesaria o por no garantizar el comportamiento esperado en produccion.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.identity_provider_intro.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_login
