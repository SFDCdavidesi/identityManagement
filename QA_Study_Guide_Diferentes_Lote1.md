# Study Guide - Unique Questions - Lote 1 (20)

Questions and answers in English. Detailed explanation in Spanish with references.

## Unique Question 1
**Concept:** Salesforce as an Identity Provider (17%)

**Question (EN):** An identity architect's client has a homegrown identity provider (IdP). Salesforce is used as the service provider (SP). The head of IT is worried that during a SP initiated single sign-on (SSO), the Security Assertion Markup Language (SAML) request content will be altered. What should the identity architect recommend to make sure that there is additional trust between the SP and the IdP? Ay Encrypt the SAML Request using certification authority (CA) signed certificate and decrypt on IdP.

**Correct Answer:** C

**Detailed Explanation (ES):**
La respuesta propuesta es **C** porque es la que mejor alinea el requerimiento del escenario con capacidades nativas de Salesforce Identity y con el protocolo indicado. Se descartan opciones que añaden complejidad innecesaria o no cumplen el control de acceso esperado.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.identity_provider_intro.htm&type=5
- https://help.salesforce.com/s/articleView?id=sf.sso_provider_enable.htm&type=5

## Unique Question 2
**Concept:** Community (Partner and Customer) (18%)

**Question (EN):** Universal Containers (UC) has decided to replace the homegrown customer portal with Salesforce Experience Cloud. UC will continue to use its third-party single sign-on (SSO) solution that stores all of its customer and partner credentials. The first time a customer logs in to the Experience Cloud site through SSO, a user record needs to be created automatically. Which solution should an identity architect recommend in order to automatically provision users in Salesforce upon login?

**Correct Answer:** D

**Detailed Explanation (ES):**
La respuesta propuesta es **D** porque es la que mejor alinea el requerimiento del escenario con capacidades nativas de Salesforce Identity y con el protocolo indicado. Se descartan opciones que añaden complejidad innecesaria o no cumplen el control de acceso esperado.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.networks_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_external

## Unique Question 3
**Concept:** Community (Partner and Customer) (18%)

**Question (EN):** An identity architect has been asked to recommend a solution that allows administrators to configure personalized alert messages to users before they land on the Experience Cloud site (formerly known as Community) homepage. What is recommended to fulfill this requirement with the least amount of customization? © Use Login Flows to add a screen that shows personalized alerts.

**Correct Answer:** A

**Detailed Explanation (ES):**
La respuesta propuesta es **A** porque es la que mejor alinea el requerimiento del escenario con capacidades nativas de Salesforce Identity y con el protocolo indicado. Se descartan opciones que añaden complejidad innecesaria o no cumplen el control de acceso esperado.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.networks_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_external

## Unique Question 4
**Concept:** Identity Management Concepts (17%)

**Question (EN):** Northern Trail Outfitters (NTO) believes a specific user account may have been compromised. NTO inactivated the user account and needs to perform a forensic analysis and identify signals that could indicate a breach has occurred. What should NTO's first step be in gathering signals that could Indicate account compromise?

**Correct Answer:** To Validate

**Detailed Explanation (ES):**
No hay evidencia suficiente en esta pasada para fijar una respuesta de alta confianza sin riesgo de error. Se mantiene pendiente de validacion manual avanzada.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.identity_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_basics

## Unique Question 5
**Concept:** Accepting Third-Party Identity in Salesforce (21%)

**Question (EN):** A company's external application Is protected by Salesforce through OAuth. The Identity architect for the project needs to limit the level of access to the data of the protected resource in a flexible way. What should be done to improve security?

**Correct Answer:** C

**Detailed Explanation (ES):**
La respuesta propuesta es **C** porque es la que mejor alinea el requerimiento del escenario con capacidades nativas de Salesforce Identity y con el protocolo indicado. Se descartan opciones que añaden complejidad innecesaria o no cumplen el control de acceso esperado.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.sso_saml.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_login

## Unique Question 6
**Concept:** Salesforce as an Identity Provider (17%)

**Question (EN):** A global company's Salesforce Identity Architect is reviewing its Salesforce production org login history and Is seeing some intermittent Security Assertion Markup Language (SAML SSO) "Replay Detected" and "Assertion Invalid” login errors. Which two Issues would cause these errors? The subject element Is missing from the assertion sent to Salesforce. The assertion sent to Salesforce contains an assertion ID previously used, The current time setting of the company's Identity provider (IdP) and Salesforce platform is out of sync by more than eight minutes. The certificate loaded into SSO configuration does not match the certificate used by the IdP. Salesforce Certified Identity and Access Management Archit«

**Correct Answer:** AB

**Detailed Explanation (ES):**
La respuesta propuesta es **AB** porque es la que mejor alinea el requerimiento del escenario con capacidades nativas de Salesforce Identity y con el protocolo indicado. Esta pregunta requiere seleccionar **2** opcion(es). Se descartan opciones que añaden complejidad innecesaria o no cumplen el control de acceso esperado.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.identity_provider_intro.htm&type=5
- https://help.salesforce.com/s/articleView?id=sf.sso_provider_enable.htm&type=5

## Unique Question 7
**Concept:** Salesforce as an Identity Provider (17%)

**Question (EN):** Universal Containers (UC) currently uses Salesforce Sales Cloud and an external billing application. Both Salesforce and the billing application are accessed several times a day to manage customers. UC would like to configure single sign-on and leverage Salesforce as the identity provider. Additionally, UC would like the billing application to be accessible from Salesforce. A redirect is acceptable. Which two Salesforce tools should an identity architect recommend to satisfy the requirements? 4@ Salesforce Canvas 8. @@ App Launcher €.( Identity Connect D.C Connected Apps ES ES ED EE by ORAKE INTERNATIONAL

**Correct Answer:** BC

**Detailed Explanation (ES):**
La respuesta propuesta es **BC** porque es la que mejor alinea el requerimiento del escenario con capacidades nativas de Salesforce Identity y con el protocolo indicado. Esta pregunta requiere seleccionar **2** opcion(es). Se descartan opciones que añaden complejidad innecesaria o no cumplen el control de acceso esperado.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.identity_provider_intro.htm&type=5
- https://help.salesforce.com/s/articleView?id=sf.sso_provider_enable.htm&type=5

## Unique Question 8
**Concept:** Identity Management Concepts (17%)

**Question (EN):** A web service Is developed that allows secure access to customer order status on the Salesforce Platform. The service connects to Salesforce through a connected app with the web server flow. The following are the required actions for the authorization flow: . User Authenticates and Authorizes Access - Request an Access Token . Salesforce Grants an Access Token |. Request an Authorization Code . Salesforce Grants Authorization Code vee What is the correct sequence for the authorization flow? O Mark this tem for later review.

**Correct Answer:** To Validate

**Detailed Explanation (ES):**
No hay evidencia suficiente en esta pasada para fijar una respuesta de alta confianza sin riesgo de error. Se mantiene pendiente de validacion manual avanzada.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.identity_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_basics

## Unique Question 9
**Concept:** Salesforce as an Identity Provider (17%)

**Question (EN):** An identity architect is setting up an integration between Salesforce and a third-party system. The third-party system needs to be able to authenticate to Salesforce and then make API calls against the REST API. One of the requirements is that the solution needs to ensure the third party service providers connected app in Salesforce minimizes the need for end user interaction and maximizes security. Which OAuth flow should be used to fulfill the requirement? JWT Bearer Flow B.O Web Server Flow €.© Username-Password Flow

**Correct Answer:** A

**Detailed Explanation (ES):**
La respuesta propuesta es **A** porque es la que mejor alinea el requerimiento del escenario con capacidades nativas de Salesforce Identity y con el protocolo indicado. Se descartan opciones que añaden complejidad innecesaria o no cumplen el control de acceso esperado.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.identity_provider_intro.htm&type=5
- https://help.salesforce.com/s/articleView?id=sf.sso_provider_enable.htm&type=5

## Unique Question 10
**Concept:** Community (Partner and Customer) (18%)

**Question (EN):** An identity professional is working on the configuration of a connected app for Universal Container's (UC) partner portal. UC wants to allow external users to access certain Salesforce data and perform limited actions. However, they also want to enforce additional security measures, such as IP restrictions and session timeout settings. Which configuration option should be used to enforce IP restrictions and session timeout settings for the connected app? Session Settings £.O Login IP Ranges €.Q Custom Permissions

**Correct Answer:** AC

**Detailed Explanation (ES):**
La respuesta propuesta es **AC** porque es la que mejor alinea el requerimiento del escenario con capacidades nativas de Salesforce Identity y con el protocolo indicado. Esta pregunta requiere seleccionar **2** opcion(es). Se descartan opciones que añaden complejidad innecesaria o no cumplen el control de acceso esperado.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.networks_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_external

## Unique Question 11
**Concept:** Accepting Third-Party Identity in Salesforce (21%)

**Question (EN):** Northern Trail Outfitters (NTO) leverages Microsoft Active Directory (AD) for management of employee usernames, passwords, permissions, and asset access. NTO also owns a third-party single sign-on (SSO) solution. The third-party party SSO solution is used for all corporate applications, including Salesforce. NTO has asked an architect to explore Salesforce Identity Connect for automatic provisioning and deprovisioning of users in Salesforce. What role does identity Connect play in the outlined requirements?

**Correct Answer:** AD

**Detailed Explanation (ES):**
La respuesta propuesta es **AD** porque es la que mejor alinea el requerimiento del escenario con capacidades nativas de Salesforce Identity y con el protocolo indicado. Esta pregunta requiere seleccionar **2** opcion(es). Se descartan opciones que añaden complejidad innecesaria o no cumplen el control de acceso esperado.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.sso_saml.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_login

## Unique Question 12
**Concept:** Salesforce as an Identity Provider (17%)

**Question (EN):** A security architect is rolling out a new multi-factor authentication (MFA) mandate, where all employees must go through a secure authentication process before accessing Salesforce. There are multiple Identity Providers (IdP) in place and the architect is considering how the "Authentication Method Reference" field (AMR) in the Login History can help. Which two considerations should the architect keep in mind? 8. [ High-assurance sessions must be configured under Session Security Level Policies.

**Correct Answer:** To Validate

**Detailed Explanation (ES):**
No hay evidencia suficiente en esta pasada para fijar una respuesta de alta confianza sin riesgo de error. Se mantiene pendiente de validacion manual avanzada.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.identity_provider_intro.htm&type=5
- https://help.salesforce.com/s/articleView?id=sf.sso_provider_enable.htm&type=5

## Unique Question 13
**Concept:** Accepting Third-Party Identity in Salesforce (21%)

**Question (EN):** Universal Containers is designing an identity architecture that involves integrating Salesforce with an external directory service. The external directory service will act as the central repository for user authentication and authorization across multiple systems within the organization. Which approach should be evaluated to establish trust between Salesforce and the external directory service? © Implementing a federated identity solution based on SAML (Security Assertion Markup Language).

**Correct Answer:** B

**Detailed Explanation (ES):**
La respuesta propuesta es **B** porque es la que mejor alinea el requerimiento del escenario con capacidades nativas de Salesforce Identity y con el protocolo indicado. Se descartan opciones que añaden complejidad innecesaria o no cumplen el control de acceso esperado.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.sso_saml.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_login

## Unique Question 14
**Concept:** Salesforce as an Identity Provider (17%)

**Question (EN):** Northern Trail Outfitters (NTO) uses a Security Assertion Markup Language (SAML)-based Identity Provider (IdP) to authenticate employees to all systems. The IdP authenticates users against a Lightweight Directory Access Protocol (LDAP) directory and has access to user information. NTO wants to minimize Salesforce license usage since only a small percentage of users need Salesforce. What is recommended to ensure new employees have immediate access to Salesforce using their current IdP?

**Correct Answer:** C

**Detailed Explanation (ES):**
La respuesta propuesta es **C** porque es la que mejor alinea el requerimiento del escenario con capacidades nativas de Salesforce Identity y con el protocolo indicado. Se descartan opciones que añaden complejidad innecesaria o no cumplen el control de acceso esperado.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.identity_provider_intro.htm&type=5
- https://help.salesforce.com/s/articleView?id=sf.sso_provider_enable.htm&type=5

## Unique Question 15
**Concept:** Salesforce as an Identity Provider (17%)

**Question (EN):** Northern Trail Outfitters manages application functional permissions centrally as Active Directory groups. The CRM_SuperUse and CRM _ Reporting SuperUser groups should respectively give the user the SuperUser and Reporting_SuperUser permission set in Salesforce. Salesforce is the service provider to a Security Assertion Markup Language (SAML) identity provider. How should an identity architect ensure the Active Directory groups are reflected correctly when a user accesses Salesforce?

**Correct Answer:** B

**Detailed Explanation (ES):**
La respuesta propuesta es **B** porque es la que mejor alinea el requerimiento del escenario con capacidades nativas de Salesforce Identity y con el protocolo indicado. Se descartan opciones que añaden complejidad innecesaria o no cumplen el control de acceso esperado.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.identity_provider_intro.htm&type=5
- https://help.salesforce.com/s/articleView?id=sf.sso_provider_enable.htm&type=5

## Unique Question 16
**Concept:** Accepting Third-Party Identity in Salesforce (21%)

**Question (EN):** A farming enterprise offers smart farming technology to its farmer customers, which includes a variety of sensors for livestock tracking, pest monitoring, climate monitoring etc. They plan to store all the data in Salesforce. They would also like to ensure timely maintenance of the installed sensors. They have engaged a Salesforce Architect to propose an appropriate way to send an alert when something goes wrong. Which OAuth flow should the architect recommend?

**Correct Answer:** To Validate

**Detailed Explanation (ES):**
No hay evidencia suficiente en esta pasada para fijar una respuesta de alta confianza sin riesgo de error. Se mantiene pendiente de validacion manual avanzada.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.sso_saml.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_login

## Unique Question 17
**Concept:** Identity Management Concepts (17%)

**Question (EN):** An insurance company has a connected app in its Salesforce environment that is used to integrate with a Google Workspace (formerly known as G Suite). An identity and access management (IAM) architect has been asked to implement automation to enable users, freeze/suspend users, disable users, and reactivate existing users in Google Workspace upon similar actions in Salesforce. Which solution is recommended to meet this requirement?

**Correct Answer:** A

**Detailed Explanation (ES):**
La respuesta propuesta es **A** porque es la que mejor alinea el requerimiento del escenario con capacidades nativas de Salesforce Identity y con el protocolo indicado. Se descartan opciones que añaden complejidad innecesaria o no cumplen el control de acceso esperado.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.identity_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_basics

## Unique Question 18
**Concept:** Accepting Third-Party Identity in Salesforce (21%)

**Question (EN):** A global fitness equipment manufacturer is planning to sell fitness tracking devices and has the following requirements: 1) Customer purchases the device. 2) Customer registers the device using their mobile app. 3) A case should automatically be created in Salesforce and associated with the customers account in cases where the device registers issues with tracking. Which OAuth flow should be used to meet these requirements?

**Correct Answer:** To Validate

**Detailed Explanation (ES):**
No hay evidencia suficiente en esta pasada para fijar una respuesta de alta confianza sin riesgo de error. Se mantiene pendiente de validacion manual avanzada.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.sso_saml.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_login

## Unique Question 19
**Concept:** Identity Management Concepts (17%)

**Question (EN):** A financial enterprise is planning to set up a user authentication mechanism to login to the Salesforce system. Due to regulatory requirements, the CIO of the company wants user administration, including passwords and authentication requests, to be managed by an external system that is only accessible via a SOAP webservice. Which authentication mechanism should an identity architect recommend to meet the requirements?

**Correct Answer:** To Validate

**Detailed Explanation (ES):**
No hay evidencia suficiente en esta pasada para fijar una respuesta de alta confianza sin riesgo de error. Se mantiene pendiente de validacion manual avanzada.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.identity_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_basics

## Unique Question 20
**Concept:** Access Management Best Practices (15%)

**Question (EN):** An identity professional, responsible for ensuring secure access to the Salesforce platform, needs to audit and verify user activity during and after login. They want to monitor login attempts, track user authentication methods, and identify suspicious behavior or unauthorized access. Which tool or feature should they leverage to achieve this objective? AO ‘Salesforce Approval Processes By Salesforce Login History

**Correct Answer:** C

**Detailed Explanation (ES):**
La respuesta propuesta es **C** porque es la que mejor alinea el requerimiento del escenario con capacidades nativas de Salesforce Identity y con el protocolo indicado. Se descartan opciones que añaden complejidad innecesaria o no cumplen el control de acceso esperado.

**References:**
- https://help.salesforce.com/s/articleView?id=sf.security_overview.htm&type=5
- https://trailhead.salesforce.com/content/learn/modules/identity_mfa
