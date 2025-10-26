# Generated FHIR module
# Do not edit manually
"""FHIR Resource models with lazy loading support.

This module provides ~300 FHIR resource type definitions. To avoid massive
startup costs, models are loaded on-demand via __getattr__.

For static type checking: Use stub file (pymedplum/fhir/__init__.pyi)
For IDE autocompletion: All types appear in autocomplete via __dir__()
For runtime usage: Import normally, models load transparently

Examples:
    Direct import (lazy loads on access):
    >>> from pymedplum.fhir import Patient

    Type annotations (work with stub file):
    >>> from pymedplum.fhir import Resource
    >>> def process(r: Resource) -> str: ...

Performance:
    - First import: ~50ms (loads model + dependencies)
    - Cached access: ~1µs (dict lookup)
    - Type checking: Instant (stub file, no code execution)
"""

import importlib
import re
import threading
from typing import TYPE_CHECKING, Any

from .base import MedplumFHIRBase

# ============================================================================
# Public API
# ============================================================================

# Lightweight runtime alias; a more specific union is used for type checking
Resource = MedplumFHIRBase

# ============================================================================
# Thread-Safe Lazy Loading Infrastructure
# ============================================================================

# Per-model loading lock to prevent redundant concurrent imports
_MODEL_LOCKS: dict[str, threading.RLock] = {}
_MODEL_LOCKS_LOCK = threading.Lock()

# Shared types namespace for Pydantic model_rebuild() forward reference resolution
_TYPES_NS: dict[str, Any] = {
    "ResourceType": str,
}

# Global rebuild coordination
_REBUILD_LOCK = threading.RLock()
_TYPES_NS_VERSION = 0
_LAST_REBUILT_VERSION = -1

# Track which models are currently being loaded to detect circular dependencies
_LOADING_STACK: set[str] = set()
_LOADING_STACK_LOCK = threading.Lock()

# Registry mapping class names to their module paths
REGISTRY: dict[str, str] = {
    "AccessPolicy": "pymedplum.fhir.accesspolicy:AccessPolicy",
    "AccessPolicyIpAccessRule": "pymedplum.fhir.accesspolicy:AccessPolicyIpAccessRule",
    "AccessPolicyResource": "pymedplum.fhir.accesspolicy:AccessPolicyResource",
    "Account": "pymedplum.fhir.account:Account",
    "AccountCoverage": "pymedplum.fhir.account:AccountCoverage",
    "AccountGuarantor": "pymedplum.fhir.account:AccountGuarantor",
    "ActivityDefinition": "pymedplum.fhir.activitydefinition:ActivityDefinition",
    "ActivityDefinitionDynamicValue": "pymedplum.fhir.activitydefinition:ActivityDefinitionDynamicValue",
    "ActivityDefinitionParticipant": "pymedplum.fhir.activitydefinition:ActivityDefinitionParticipant",
    "Address": "pymedplum.fhir.address:Address",
    "AdverseEvent": "pymedplum.fhir.adverseevent:AdverseEvent",
    "AdverseEventSuspectEntity": "pymedplum.fhir.adverseevent:AdverseEventSuspectEntity",
    "AdverseEventSuspectEntityCausality": "pymedplum.fhir.adverseevent:AdverseEventSuspectEntityCausality",
    "Age": "pymedplum.fhir.age:Age",
    "Agent": "pymedplum.fhir.agent:Agent",
    "AgentChannel": "pymedplum.fhir.agent:AgentChannel",
    "AgentSetting": "pymedplum.fhir.agent:AgentSetting",
    "AllergyIntolerance": "pymedplum.fhir.allergyintolerance:AllergyIntolerance",
    "AllergyIntoleranceReaction": "pymedplum.fhir.allergyintolerance:AllergyIntoleranceReaction",
    "Annotation": "pymedplum.fhir.annotation:Annotation",
    "Appointment": "pymedplum.fhir.appointment:Appointment",
    "AppointmentParticipant": "pymedplum.fhir.appointment:AppointmentParticipant",
    "AppointmentResponse": "pymedplum.fhir.appointmentresponse:AppointmentResponse",
    "AsyncJob": "pymedplum.fhir.asyncjob:AsyncJob",
    "Attachment": "pymedplum.fhir.attachment:Attachment",
    "AuditEvent": "pymedplum.fhir.auditevent:AuditEvent",
    "AuditEventAgent": "pymedplum.fhir.auditevent:AuditEventAgent",
    "AuditEventAgentNetwork": "pymedplum.fhir.auditevent:AuditEventAgentNetwork",
    "AuditEventEntity": "pymedplum.fhir.auditevent:AuditEventEntity",
    "AuditEventEntityDetail": "pymedplum.fhir.auditevent:AuditEventEntityDetail",
    "AuditEventSource": "pymedplum.fhir.auditevent:AuditEventSource",
    "BackboneElement": "pymedplum.fhir.backboneelement:BackboneElement",
    "Basic": "pymedplum.fhir.basic:Basic",
    "Binary": "pymedplum.fhir.binary:Binary",
    "BiologicallyDerivedProduct": "pymedplum.fhir.biologicallyderivedproduct:BiologicallyDerivedProduct",
    "BiologicallyDerivedProductCollection": "pymedplum.fhir.biologicallyderivedproduct:BiologicallyDerivedProductCollection",
    "BiologicallyDerivedProductManipulation": "pymedplum.fhir.biologicallyderivedproduct:BiologicallyDerivedProductManipulation",
    "BiologicallyDerivedProductProcessing": "pymedplum.fhir.biologicallyderivedproduct:BiologicallyDerivedProductProcessing",
    "BiologicallyDerivedProductStorage": "pymedplum.fhir.biologicallyderivedproduct:BiologicallyDerivedProductStorage",
    "BodyStructure": "pymedplum.fhir.bodystructure:BodyStructure",
    "Bot": "pymedplum.fhir.bot:Bot",
    "BulkDataExport": "pymedplum.fhir.bulkdataexport:BulkDataExport",
    "BulkDataExportDeleted": "pymedplum.fhir.bulkdataexport:BulkDataExportDeleted",
    "BulkDataExportError": "pymedplum.fhir.bulkdataexport:BulkDataExportError",
    "BulkDataExportOutput": "pymedplum.fhir.bulkdataexport:BulkDataExportOutput",
    "Bundle": "pymedplum.fhir.bundle:Bundle",
    "BundleEntry": "pymedplum.fhir.bundle:BundleEntry",
    "BundleEntryRequest": "pymedplum.fhir.bundle:BundleEntryRequest",
    "BundleEntryResponse": "pymedplum.fhir.bundle:BundleEntryResponse",
    "BundleEntrySearch": "pymedplum.fhir.bundle:BundleEntrySearch",
    "BundleLink": "pymedplum.fhir.bundle:BundleLink",
    "CapabilityStatement": "pymedplum.fhir.capabilitystatement:CapabilityStatement",
    "CapabilityStatementDocument": "pymedplum.fhir.capabilitystatement:CapabilityStatementDocument",
    "CapabilityStatementImplementation": "pymedplum.fhir.capabilitystatement:CapabilityStatementImplementation",
    "CapabilityStatementMessaging": "pymedplum.fhir.capabilitystatement:CapabilityStatementMessaging",
    "CapabilityStatementMessagingEndpoint": "pymedplum.fhir.capabilitystatement:CapabilityStatementMessagingEndpoint",
    "CapabilityStatementMessagingSupportedMessage": "pymedplum.fhir.capabilitystatement:CapabilityStatementMessagingSupportedMessage",
    "CapabilityStatementRest": "pymedplum.fhir.capabilitystatement:CapabilityStatementRest",
    "CapabilityStatementRestInteraction": "pymedplum.fhir.capabilitystatement:CapabilityStatementRestInteraction",
    "CapabilityStatementRestResource": "pymedplum.fhir.capabilitystatement:CapabilityStatementRestResource",
    "CapabilityStatementRestResourceInteraction": "pymedplum.fhir.capabilitystatement:CapabilityStatementRestResourceInteraction",
    "CapabilityStatementRestResourceOperation": "pymedplum.fhir.capabilitystatement:CapabilityStatementRestResourceOperation",
    "CapabilityStatementRestResourceSearchParam": "pymedplum.fhir.capabilitystatement:CapabilityStatementRestResourceSearchParam",
    "CapabilityStatementRestSecurity": "pymedplum.fhir.capabilitystatement:CapabilityStatementRestSecurity",
    "CapabilityStatementSoftware": "pymedplum.fhir.capabilitystatement:CapabilityStatementSoftware",
    "CarePlan": "pymedplum.fhir.careplan:CarePlan",
    "CarePlanActivity": "pymedplum.fhir.careplan:CarePlanActivity",
    "CarePlanActivityDetail": "pymedplum.fhir.careplan:CarePlanActivityDetail",
    "CareTeam": "pymedplum.fhir.careteam:CareTeam",
    "CareTeamParticipant": "pymedplum.fhir.careteam:CareTeamParticipant",
    "CatalogEntry": "pymedplum.fhir.catalogentry:CatalogEntry",
    "CatalogEntryRelatedEntry": "pymedplum.fhir.catalogentry:CatalogEntryRelatedEntry",
    "ChargeItem": "pymedplum.fhir.chargeitem:ChargeItem",
    "ChargeItemDefinition": "pymedplum.fhir.chargeitemdefinition:ChargeItemDefinition",
    "ChargeItemDefinitionApplicability": "pymedplum.fhir.chargeitemdefinition:ChargeItemDefinitionApplicability",
    "ChargeItemDefinitionPropertyGroup": "pymedplum.fhir.chargeitemdefinition:ChargeItemDefinitionPropertyGroup",
    "ChargeItemDefinitionPropertyGroupPriceComponent": "pymedplum.fhir.chargeitemdefinition:ChargeItemDefinitionPropertyGroupPriceComponent",
    "ChargeItemPerformer": "pymedplum.fhir.chargeitem:ChargeItemPerformer",
    "Claim": "pymedplum.fhir.claim:Claim",
    "ClaimAccident": "pymedplum.fhir.claim:ClaimAccident",
    "ClaimCareTeam": "pymedplum.fhir.claim:ClaimCareTeam",
    "ClaimDiagnosis": "pymedplum.fhir.claim:ClaimDiagnosis",
    "ClaimInsurance": "pymedplum.fhir.claim:ClaimInsurance",
    "ClaimItem": "pymedplum.fhir.claim:ClaimItem",
    "ClaimItemDetail": "pymedplum.fhir.claim:ClaimItemDetail",
    "ClaimItemDetailSubDetail": "pymedplum.fhir.claim:ClaimItemDetailSubDetail",
    "ClaimPayee": "pymedplum.fhir.claim:ClaimPayee",
    "ClaimProcedure": "pymedplum.fhir.claim:ClaimProcedure",
    "ClaimRelated": "pymedplum.fhir.claim:ClaimRelated",
    "ClaimResponse": "pymedplum.fhir.claimresponse:ClaimResponse",
    "ClaimResponseAddItem": "pymedplum.fhir.claimresponse:ClaimResponseAddItem",
    "ClaimResponseAddItemDetail": "pymedplum.fhir.claimresponse:ClaimResponseAddItemDetail",
    "ClaimResponseAddItemDetailSubDetail": "pymedplum.fhir.claimresponse:ClaimResponseAddItemDetailSubDetail",
    "ClaimResponseError": "pymedplum.fhir.claimresponse:ClaimResponseError",
    "ClaimResponseInsurance": "pymedplum.fhir.claimresponse:ClaimResponseInsurance",
    "ClaimResponseItem": "pymedplum.fhir.claimresponse:ClaimResponseItem",
    "ClaimResponseItemAdjudication": "pymedplum.fhir.claimresponse:ClaimResponseItemAdjudication",
    "ClaimResponseItemDetail": "pymedplum.fhir.claimresponse:ClaimResponseItemDetail",
    "ClaimResponseItemDetailSubDetail": "pymedplum.fhir.claimresponse:ClaimResponseItemDetailSubDetail",
    "ClaimResponsePayment": "pymedplum.fhir.claimresponse:ClaimResponsePayment",
    "ClaimResponseProcessNote": "pymedplum.fhir.claimresponse:ClaimResponseProcessNote",
    "ClaimResponseTotal": "pymedplum.fhir.claimresponse:ClaimResponseTotal",
    "ClaimSupportingInfo": "pymedplum.fhir.claim:ClaimSupportingInfo",
    "ClientApplication": "pymedplum.fhir.clientapplication:ClientApplication",
    "ClientApplicationSignInForm": "pymedplum.fhir.clientapplication:ClientApplicationSignInForm",
    "ClinicalImpression": "pymedplum.fhir.clinicalimpression:ClinicalImpression",
    "ClinicalImpressionFinding": "pymedplum.fhir.clinicalimpression:ClinicalImpressionFinding",
    "ClinicalImpressionInvestigation": "pymedplum.fhir.clinicalimpression:ClinicalImpressionInvestigation",
    "CodeSystem": "pymedplum.fhir.codesystem:CodeSystem",
    "CodeSystemConcept": "pymedplum.fhir.codesystem:CodeSystemConcept",
    "CodeSystemConceptDesignation": "pymedplum.fhir.codesystem:CodeSystemConceptDesignation",
    "CodeSystemConceptProperty": "pymedplum.fhir.codesystem:CodeSystemConceptProperty",
    "CodeSystemFilter": "pymedplum.fhir.codesystem:CodeSystemFilter",
    "CodeSystemProperty": "pymedplum.fhir.codesystem:CodeSystemProperty",
    "CodeableConcept": "pymedplum.fhir.codeableconcept:CodeableConcept",
    "Coding": "pymedplum.fhir.coding:Coding",
    "Communication": "pymedplum.fhir.communication:Communication",
    "CommunicationPayload": "pymedplum.fhir.communication:CommunicationPayload",
    "CommunicationRequest": "pymedplum.fhir.communicationrequest:CommunicationRequest",
    "CommunicationRequestPayload": "pymedplum.fhir.communicationrequest:CommunicationRequestPayload",
    "CompartmentDefinition": "pymedplum.fhir.compartmentdefinition:CompartmentDefinition",
    "CompartmentDefinitionResource": "pymedplum.fhir.compartmentdefinition:CompartmentDefinitionResource",
    "Composition": "pymedplum.fhir.composition:Composition",
    "CompositionAttester": "pymedplum.fhir.composition:CompositionAttester",
    "CompositionEvent": "pymedplum.fhir.composition:CompositionEvent",
    "CompositionRelatesTo": "pymedplum.fhir.composition:CompositionRelatesTo",
    "CompositionSection": "pymedplum.fhir.composition:CompositionSection",
    "ConceptMap": "pymedplum.fhir.conceptmap:ConceptMap",
    "ConceptMapGroup": "pymedplum.fhir.conceptmap:ConceptMapGroup",
    "ConceptMapGroupElement": "pymedplum.fhir.conceptmap:ConceptMapGroupElement",
    "ConceptMapGroupElementTarget": "pymedplum.fhir.conceptmap:ConceptMapGroupElementTarget",
    "ConceptMapGroupElementTargetDependsOn": "pymedplum.fhir.conceptmap:ConceptMapGroupElementTargetDependsOn",
    "ConceptMapGroupUnmapped": "pymedplum.fhir.conceptmap:ConceptMapGroupUnmapped",
    "Condition": "pymedplum.fhir.condition:Condition",
    "ConditionEvidence": "pymedplum.fhir.condition:ConditionEvidence",
    "ConditionStage": "pymedplum.fhir.condition:ConditionStage",
    "Consent": "pymedplum.fhir.consent:Consent",
    "ConsentPolicy": "pymedplum.fhir.consent:ConsentPolicy",
    "ConsentProvision": "pymedplum.fhir.consent:ConsentProvision",
    "ConsentProvisionActor": "pymedplum.fhir.consent:ConsentProvisionActor",
    "ConsentProvisionData": "pymedplum.fhir.consent:ConsentProvisionData",
    "ConsentVerification": "pymedplum.fhir.consent:ConsentVerification",
    "ContactDetail": "pymedplum.fhir.contactdetail:ContactDetail",
    "ContactPoint": "pymedplum.fhir.contactpoint:ContactPoint",
    "Contract": "pymedplum.fhir.contract:Contract",
    "ContractContentDefinition": "pymedplum.fhir.contract:ContractContentDefinition",
    "ContractFriendly": "pymedplum.fhir.contract:ContractFriendly",
    "ContractLegal": "pymedplum.fhir.contract:ContractLegal",
    "ContractRule": "pymedplum.fhir.contract:ContractRule",
    "ContractSigner": "pymedplum.fhir.contract:ContractSigner",
    "ContractTerm": "pymedplum.fhir.contract:ContractTerm",
    "ContractTermAction": "pymedplum.fhir.contract:ContractTermAction",
    "ContractTermActionSubject": "pymedplum.fhir.contract:ContractTermActionSubject",
    "ContractTermAsset": "pymedplum.fhir.contract:ContractTermAsset",
    "ContractTermAssetContext": "pymedplum.fhir.contract:ContractTermAssetContext",
    "ContractTermAssetValuedItem": "pymedplum.fhir.contract:ContractTermAssetValuedItem",
    "ContractTermOffer": "pymedplum.fhir.contract:ContractTermOffer",
    "ContractTermOfferAnswer": "pymedplum.fhir.contract:ContractTermOfferAnswer",
    "ContractTermOfferParty": "pymedplum.fhir.contract:ContractTermOfferParty",
    "ContractTermSecurityLabel": "pymedplum.fhir.contract:ContractTermSecurityLabel",
    "Contributor": "pymedplum.fhir.contributor:Contributor",
    "Count": "pymedplum.fhir.count:Count",
    "Coverage": "pymedplum.fhir.coverage:Coverage",
    "CoverageClass": "pymedplum.fhir.coverage:CoverageClass",
    "CoverageCostToBeneficiary": "pymedplum.fhir.coverage:CoverageCostToBeneficiary",
    "CoverageCostToBeneficiaryException": "pymedplum.fhir.coverage:CoverageCostToBeneficiaryException",
    "CoverageEligibilityRequest": "pymedplum.fhir.coverageeligibilityrequest:CoverageEligibilityRequest",
    "CoverageEligibilityRequestInsurance": "pymedplum.fhir.coverageeligibilityrequest:CoverageEligibilityRequestInsurance",
    "CoverageEligibilityRequestItem": "pymedplum.fhir.coverageeligibilityrequest:CoverageEligibilityRequestItem",
    "CoverageEligibilityRequestItemDiagnosis": "pymedplum.fhir.coverageeligibilityrequest:CoverageEligibilityRequestItemDiagnosis",
    "CoverageEligibilityRequestSupportingInfo": "pymedplum.fhir.coverageeligibilityrequest:CoverageEligibilityRequestSupportingInfo",
    "CoverageEligibilityResponse": "pymedplum.fhir.coverageeligibilityresponse:CoverageEligibilityResponse",
    "CoverageEligibilityResponseError": "pymedplum.fhir.coverageeligibilityresponse:CoverageEligibilityResponseError",
    "CoverageEligibilityResponseInsurance": "pymedplum.fhir.coverageeligibilityresponse:CoverageEligibilityResponseInsurance",
    "CoverageEligibilityResponseInsuranceItem": "pymedplum.fhir.coverageeligibilityresponse:CoverageEligibilityResponseInsuranceItem",
    "CoverageEligibilityResponseInsuranceItemBenefit": "pymedplum.fhir.coverageeligibilityresponse:CoverageEligibilityResponseInsuranceItemBenefit",
    "DataRequirement": "pymedplum.fhir.datarequirement:DataRequirement",
    "DataRequirementCodeFilter": "pymedplum.fhir.datarequirement:DataRequirementCodeFilter",
    "DataRequirementDateFilter": "pymedplum.fhir.datarequirement:DataRequirementDateFilter",
    "DataRequirementSort": "pymedplum.fhir.datarequirement:DataRequirementSort",
    "DetectedIssue": "pymedplum.fhir.detectedissue:DetectedIssue",
    "DetectedIssueEvidence": "pymedplum.fhir.detectedissue:DetectedIssueEvidence",
    "DetectedIssueMitigation": "pymedplum.fhir.detectedissue:DetectedIssueMitigation",
    "Device": "pymedplum.fhir.device:Device",
    "DeviceDefinition": "pymedplum.fhir.devicedefinition:DeviceDefinition",
    "DeviceDefinitionCapability": "pymedplum.fhir.devicedefinition:DeviceDefinitionCapability",
    "DeviceDefinitionClassification": "pymedplum.fhir.devicedefinition:DeviceDefinitionClassification",
    "DeviceDefinitionDeviceName": "pymedplum.fhir.devicedefinition:DeviceDefinitionDeviceName",
    "DeviceDefinitionMaterial": "pymedplum.fhir.devicedefinition:DeviceDefinitionMaterial",
    "DeviceDefinitionProperty": "pymedplum.fhir.devicedefinition:DeviceDefinitionProperty",
    "DeviceDefinitionSpecialization": "pymedplum.fhir.devicedefinition:DeviceDefinitionSpecialization",
    "DeviceDefinitionUdiDeviceIdentifier": "pymedplum.fhir.devicedefinition:DeviceDefinitionUdiDeviceIdentifier",
    "DeviceDeviceName": "pymedplum.fhir.device:DeviceDeviceName",
    "DeviceMetric": "pymedplum.fhir.devicemetric:DeviceMetric",
    "DeviceMetricCalibration": "pymedplum.fhir.devicemetric:DeviceMetricCalibration",
    "DeviceProperty": "pymedplum.fhir.device:DeviceProperty",
    "DeviceRequest": "pymedplum.fhir.devicerequest:DeviceRequest",
    "DeviceRequestParameter": "pymedplum.fhir.devicerequest:DeviceRequestParameter",
    "DeviceSpecialization": "pymedplum.fhir.device:DeviceSpecialization",
    "DeviceUdiCarrier": "pymedplum.fhir.device:DeviceUdiCarrier",
    "DeviceUseStatement": "pymedplum.fhir.deviceusestatement:DeviceUseStatement",
    "DeviceVersion": "pymedplum.fhir.device:DeviceVersion",
    "DiagnosticReport": "pymedplum.fhir.diagnosticreport:DiagnosticReport",
    "DiagnosticReportMedia": "pymedplum.fhir.diagnosticreport:DiagnosticReportMedia",
    "Distance": "pymedplum.fhir.distance:Distance",
    "DocumentManifest": "pymedplum.fhir.documentmanifest:DocumentManifest",
    "DocumentManifestRelated": "pymedplum.fhir.documentmanifest:DocumentManifestRelated",
    "DocumentReference": "pymedplum.fhir.documentreference:DocumentReference",
    "DocumentReferenceContent": "pymedplum.fhir.documentreference:DocumentReferenceContent",
    "DocumentReferenceContext": "pymedplum.fhir.documentreference:DocumentReferenceContext",
    "DocumentReferenceRelatesTo": "pymedplum.fhir.documentreference:DocumentReferenceRelatesTo",
    "DomainConfiguration": "pymedplum.fhir.domainconfiguration:DomainConfiguration",
    "Dosage": "pymedplum.fhir.dosage:Dosage",
    "DosageDoseAndRate": "pymedplum.fhir.dosage:DosageDoseAndRate",
    "Duration": "pymedplum.fhir.duration:Duration",
    "EffectEvidenceSynthesis": "pymedplum.fhir.effectevidencesynthesis:EffectEvidenceSynthesis",
    "EffectEvidenceSynthesisCertainty": "pymedplum.fhir.effectevidencesynthesis:EffectEvidenceSynthesisCertainty",
    "EffectEvidenceSynthesisCertaintyCertaintySubcomponent": "pymedplum.fhir.effectevidencesynthesis:EffectEvidenceSynthesisCertaintyCertaintySubcomponent",
    "EffectEvidenceSynthesisEffectEstimate": "pymedplum.fhir.effectevidencesynthesis:EffectEvidenceSynthesisEffectEstimate",
    "EffectEvidenceSynthesisEffectEstimatePrecisionEstimate": "pymedplum.fhir.effectevidencesynthesis:EffectEvidenceSynthesisEffectEstimatePrecisionEstimate",
    "EffectEvidenceSynthesisResultsByExposure": "pymedplum.fhir.effectevidencesynthesis:EffectEvidenceSynthesisResultsByExposure",
    "EffectEvidenceSynthesisSampleSize": "pymedplum.fhir.effectevidencesynthesis:EffectEvidenceSynthesisSampleSize",
    "Element": "pymedplum.fhir.element:Element",
    "ElementDefinition": "pymedplum.fhir.elementdefinition:ElementDefinition",
    "ElementDefinitionBase": "pymedplum.fhir.elementdefinition:ElementDefinitionBase",
    "ElementDefinitionBinding": "pymedplum.fhir.elementdefinition:ElementDefinitionBinding",
    "ElementDefinitionConstraint": "pymedplum.fhir.elementdefinition:ElementDefinitionConstraint",
    "ElementDefinitionExample": "pymedplum.fhir.elementdefinition:ElementDefinitionExample",
    "ElementDefinitionMapping": "pymedplum.fhir.elementdefinition:ElementDefinitionMapping",
    "ElementDefinitionSlicing": "pymedplum.fhir.elementdefinition:ElementDefinitionSlicing",
    "ElementDefinitionSlicingDiscriminator": "pymedplum.fhir.elementdefinition:ElementDefinitionSlicingDiscriminator",
    "ElementDefinitionType": "pymedplum.fhir.elementdefinition:ElementDefinitionType",
    "Encounter": "pymedplum.fhir.encounter:Encounter",
    "EncounterClassHistory": "pymedplum.fhir.encounter:EncounterClassHistory",
    "EncounterDiagnosis": "pymedplum.fhir.encounter:EncounterDiagnosis",
    "EncounterHospitalization": "pymedplum.fhir.encounter:EncounterHospitalization",
    "EncounterLocation": "pymedplum.fhir.encounter:EncounterLocation",
    "EncounterParticipant": "pymedplum.fhir.encounter:EncounterParticipant",
    "EncounterStatusHistory": "pymedplum.fhir.encounter:EncounterStatusHistory",
    "Endpoint": "pymedplum.fhir.endpoint:Endpoint",
    "EnrollmentRequest": "pymedplum.fhir.enrollmentrequest:EnrollmentRequest",
    "EnrollmentResponse": "pymedplum.fhir.enrollmentresponse:EnrollmentResponse",
    "EpisodeOfCare": "pymedplum.fhir.episodeofcare:EpisodeOfCare",
    "EpisodeOfCareDiagnosis": "pymedplum.fhir.episodeofcare:EpisodeOfCareDiagnosis",
    "EpisodeOfCareStatusHistory": "pymedplum.fhir.episodeofcare:EpisodeOfCareStatusHistory",
    "EventDefinition": "pymedplum.fhir.eventdefinition:EventDefinition",
    "Evidence": "pymedplum.fhir.evidence:Evidence",
    "EvidenceVariable": "pymedplum.fhir.evidencevariable:EvidenceVariable",
    "EvidenceVariableCharacteristic": "pymedplum.fhir.evidencevariable:EvidenceVariableCharacteristic",
    "EvidenceVariableCharacteristicDefinitionByCombination": "pymedplum.fhir.evidencevariable:EvidenceVariableCharacteristicDefinitionByCombination",
    "EvidenceVariableCharacteristicDefinitionByTypeAndValue": "pymedplum.fhir.evidencevariable:EvidenceVariableCharacteristicDefinitionByTypeAndValue",
    "EvidenceVariableCharacteristicTimeFromEvent": "pymedplum.fhir.evidencevariable:EvidenceVariableCharacteristicTimeFromEvent",
    "ExampleScenario": "pymedplum.fhir.examplescenario:ExampleScenario",
    "ExampleScenarioActor": "pymedplum.fhir.examplescenario:ExampleScenarioActor",
    "ExampleScenarioInstance": "pymedplum.fhir.examplescenario:ExampleScenarioInstance",
    "ExampleScenarioInstanceContainedInstance": "pymedplum.fhir.examplescenario:ExampleScenarioInstanceContainedInstance",
    "ExampleScenarioInstanceVersion": "pymedplum.fhir.examplescenario:ExampleScenarioInstanceVersion",
    "ExampleScenarioProcess": "pymedplum.fhir.examplescenario:ExampleScenarioProcess",
    "ExampleScenarioProcessStep": "pymedplum.fhir.examplescenario:ExampleScenarioProcessStep",
    "ExampleScenarioProcessStepAlternative": "pymedplum.fhir.examplescenario:ExampleScenarioProcessStepAlternative",
    "ExampleScenarioProcessStepOperation": "pymedplum.fhir.examplescenario:ExampleScenarioProcessStepOperation",
    "ExplanationOfBenefit": "pymedplum.fhir.explanationofbenefit:ExplanationOfBenefit",
    "ExplanationOfBenefitAccident": "pymedplum.fhir.explanationofbenefit:ExplanationOfBenefitAccident",
    "ExplanationOfBenefitAddItem": "pymedplum.fhir.explanationofbenefit:ExplanationOfBenefitAddItem",
    "ExplanationOfBenefitAddItemDetail": "pymedplum.fhir.explanationofbenefit:ExplanationOfBenefitAddItemDetail",
    "ExplanationOfBenefitAddItemDetailSubDetail": "pymedplum.fhir.explanationofbenefit:ExplanationOfBenefitAddItemDetailSubDetail",
    "ExplanationOfBenefitBenefitBalance": "pymedplum.fhir.explanationofbenefit:ExplanationOfBenefitBenefitBalance",
    "ExplanationOfBenefitBenefitBalanceFinancial": "pymedplum.fhir.explanationofbenefit:ExplanationOfBenefitBenefitBalanceFinancial",
    "ExplanationOfBenefitCareTeam": "pymedplum.fhir.explanationofbenefit:ExplanationOfBenefitCareTeam",
    "ExplanationOfBenefitDiagnosis": "pymedplum.fhir.explanationofbenefit:ExplanationOfBenefitDiagnosis",
    "ExplanationOfBenefitInsurance": "pymedplum.fhir.explanationofbenefit:ExplanationOfBenefitInsurance",
    "ExplanationOfBenefitItem": "pymedplum.fhir.explanationofbenefit:ExplanationOfBenefitItem",
    "ExplanationOfBenefitItemAdjudication": "pymedplum.fhir.explanationofbenefit:ExplanationOfBenefitItemAdjudication",
    "ExplanationOfBenefitItemDetail": "pymedplum.fhir.explanationofbenefit:ExplanationOfBenefitItemDetail",
    "ExplanationOfBenefitItemDetailSubDetail": "pymedplum.fhir.explanationofbenefit:ExplanationOfBenefitItemDetailSubDetail",
    "ExplanationOfBenefitPayee": "pymedplum.fhir.explanationofbenefit:ExplanationOfBenefitPayee",
    "ExplanationOfBenefitPayment": "pymedplum.fhir.explanationofbenefit:ExplanationOfBenefitPayment",
    "ExplanationOfBenefitProcedure": "pymedplum.fhir.explanationofbenefit:ExplanationOfBenefitProcedure",
    "ExplanationOfBenefitProcessNote": "pymedplum.fhir.explanationofbenefit:ExplanationOfBenefitProcessNote",
    "ExplanationOfBenefitRelated": "pymedplum.fhir.explanationofbenefit:ExplanationOfBenefitRelated",
    "ExplanationOfBenefitSupportingInfo": "pymedplum.fhir.explanationofbenefit:ExplanationOfBenefitSupportingInfo",
    "ExplanationOfBenefitTotal": "pymedplum.fhir.explanationofbenefit:ExplanationOfBenefitTotal",
    "Expression": "pymedplum.fhir.expression:Expression",
    "Extension": "pymedplum.fhir.extension:Extension",
    "FamilyMemberHistory": "pymedplum.fhir.familymemberhistory:FamilyMemberHistory",
    "FamilyMemberHistoryCondition": "pymedplum.fhir.familymemberhistory:FamilyMemberHistoryCondition",
    "Flag": "pymedplum.fhir.flag:Flag",
    "Goal": "pymedplum.fhir.goal:Goal",
    "GoalTarget": "pymedplum.fhir.goal:GoalTarget",
    "GraphDefinition": "pymedplum.fhir.graphdefinition:GraphDefinition",
    "GraphDefinitionLink": "pymedplum.fhir.graphdefinition:GraphDefinitionLink",
    "GraphDefinitionLinkTarget": "pymedplum.fhir.graphdefinition:GraphDefinitionLinkTarget",
    "GraphDefinitionLinkTargetCompartment": "pymedplum.fhir.graphdefinition:GraphDefinitionLinkTargetCompartment",
    "Group": "pymedplum.fhir.group:Group",
    "GroupCharacteristic": "pymedplum.fhir.group:GroupCharacteristic",
    "GroupMember": "pymedplum.fhir.group:GroupMember",
    "GuidanceResponse": "pymedplum.fhir.guidanceresponse:GuidanceResponse",
    "HealthcareService": "pymedplum.fhir.healthcareservice:HealthcareService",
    "HealthcareServiceAvailableTime": "pymedplum.fhir.healthcareservice:HealthcareServiceAvailableTime",
    "HealthcareServiceEligibility": "pymedplum.fhir.healthcareservice:HealthcareServiceEligibility",
    "HealthcareServiceNotAvailable": "pymedplum.fhir.healthcareservice:HealthcareServiceNotAvailable",
    "HumanName": "pymedplum.fhir.humanname:HumanName",
    "Identifier": "pymedplum.fhir.identifier:Identifier",
    "IdentityProvider": "pymedplum.fhir.identityprovider:IdentityProvider",
    "ImagingStudy": "pymedplum.fhir.imagingstudy:ImagingStudy",
    "ImagingStudySeries": "pymedplum.fhir.imagingstudy:ImagingStudySeries",
    "ImagingStudySeriesInstance": "pymedplum.fhir.imagingstudy:ImagingStudySeriesInstance",
    "ImagingStudySeriesPerformer": "pymedplum.fhir.imagingstudy:ImagingStudySeriesPerformer",
    "Immunization": "pymedplum.fhir.immunization:Immunization",
    "ImmunizationEducation": "pymedplum.fhir.immunization:ImmunizationEducation",
    "ImmunizationEvaluation": "pymedplum.fhir.immunizationevaluation:ImmunizationEvaluation",
    "ImmunizationPerformer": "pymedplum.fhir.immunization:ImmunizationPerformer",
    "ImmunizationProtocolApplied": "pymedplum.fhir.immunization:ImmunizationProtocolApplied",
    "ImmunizationReaction": "pymedplum.fhir.immunization:ImmunizationReaction",
    "ImmunizationRecommendation": "pymedplum.fhir.immunizationrecommendation:ImmunizationRecommendation",
    "ImmunizationRecommendationRecommendation": "pymedplum.fhir.immunizationrecommendation:ImmunizationRecommendationRecommendation",
    "ImmunizationRecommendationRecommendationDateCriterion": "pymedplum.fhir.immunizationrecommendation:ImmunizationRecommendationRecommendationDateCriterion",
    "ImplementationGuide": "pymedplum.fhir.implementationguide:ImplementationGuide",
    "ImplementationGuideDefinition": "pymedplum.fhir.implementationguide:ImplementationGuideDefinition",
    "ImplementationGuideDefinitionGrouping": "pymedplum.fhir.implementationguide:ImplementationGuideDefinitionGrouping",
    "ImplementationGuideDefinitionPage": "pymedplum.fhir.implementationguide:ImplementationGuideDefinitionPage",
    "ImplementationGuideDefinitionParameter": "pymedplum.fhir.implementationguide:ImplementationGuideDefinitionParameter",
    "ImplementationGuideDefinitionResource": "pymedplum.fhir.implementationguide:ImplementationGuideDefinitionResource",
    "ImplementationGuideDefinitionTemplate": "pymedplum.fhir.implementationguide:ImplementationGuideDefinitionTemplate",
    "ImplementationGuideDependsOn": "pymedplum.fhir.implementationguide:ImplementationGuideDependsOn",
    "ImplementationGuideGlobal": "pymedplum.fhir.implementationguide:ImplementationGuideGlobal",
    "ImplementationGuideManifest": "pymedplum.fhir.implementationguide:ImplementationGuideManifest",
    "ImplementationGuideManifestPage": "pymedplum.fhir.implementationguide:ImplementationGuideManifestPage",
    "ImplementationGuideManifestResource": "pymedplum.fhir.implementationguide:ImplementationGuideManifestResource",
    "InsurancePlan": "pymedplum.fhir.insuranceplan:InsurancePlan",
    "InsurancePlanContact": "pymedplum.fhir.insuranceplan:InsurancePlanContact",
    "InsurancePlanCoverage": "pymedplum.fhir.insuranceplan:InsurancePlanCoverage",
    "InsurancePlanCoverageBenefit": "pymedplum.fhir.insuranceplan:InsurancePlanCoverageBenefit",
    "InsurancePlanCoverageBenefitLimit": "pymedplum.fhir.insuranceplan:InsurancePlanCoverageBenefitLimit",
    "InsurancePlanPlan": "pymedplum.fhir.insuranceplan:InsurancePlanPlan",
    "InsurancePlanPlanGeneralCost": "pymedplum.fhir.insuranceplan:InsurancePlanPlanGeneralCost",
    "InsurancePlanPlanSpecificCost": "pymedplum.fhir.insuranceplan:InsurancePlanPlanSpecificCost",
    "InsurancePlanPlanSpecificCostBenefit": "pymedplum.fhir.insuranceplan:InsurancePlanPlanSpecificCostBenefit",
    "InsurancePlanPlanSpecificCostBenefitCost": "pymedplum.fhir.insuranceplan:InsurancePlanPlanSpecificCostBenefitCost",
    "Invoice": "pymedplum.fhir.invoice:Invoice",
    "InvoiceLineItem": "pymedplum.fhir.invoice:InvoiceLineItem",
    "InvoiceLineItemPriceComponent": "pymedplum.fhir.invoice:InvoiceLineItemPriceComponent",
    "InvoiceParticipant": "pymedplum.fhir.invoice:InvoiceParticipant",
    "JsonWebKey": "pymedplum.fhir.jsonwebkey:JsonWebKey",
    "Library": "pymedplum.fhir.library:Library",
    "Linkage": "pymedplum.fhir.linkage:Linkage",
    "LinkageItem": "pymedplum.fhir.linkage:LinkageItem",
    "List": "pymedplum.fhir.list:List",
    "ListEntry": "pymedplum.fhir.list:ListEntry",
    "Location": "pymedplum.fhir.location:Location",
    "LocationHoursOfOperation": "pymedplum.fhir.location:LocationHoursOfOperation",
    "LocationPosition": "pymedplum.fhir.location:LocationPosition",
    "Login": "pymedplum.fhir.login:Login",
    "MarketingStatus": "pymedplum.fhir.marketingstatus:MarketingStatus",
    "Measure": "pymedplum.fhir.measure:Measure",
    "MeasureGroup": "pymedplum.fhir.measure:MeasureGroup",
    "MeasureGroupPopulation": "pymedplum.fhir.measure:MeasureGroupPopulation",
    "MeasureGroupStratifier": "pymedplum.fhir.measure:MeasureGroupStratifier",
    "MeasureGroupStratifierComponent": "pymedplum.fhir.measure:MeasureGroupStratifierComponent",
    "MeasureReport": "pymedplum.fhir.measurereport:MeasureReport",
    "MeasureReportGroup": "pymedplum.fhir.measurereport:MeasureReportGroup",
    "MeasureReportGroupPopulation": "pymedplum.fhir.measurereport:MeasureReportGroupPopulation",
    "MeasureReportGroupStratifier": "pymedplum.fhir.measurereport:MeasureReportGroupStratifier",
    "MeasureReportGroupStratifierStratum": "pymedplum.fhir.measurereport:MeasureReportGroupStratifierStratum",
    "MeasureReportGroupStratifierStratumComponent": "pymedplum.fhir.measurereport:MeasureReportGroupStratifierStratumComponent",
    "MeasureReportGroupStratifierStratumPopulation": "pymedplum.fhir.measurereport:MeasureReportGroupStratifierStratumPopulation",
    "MeasureSupplementalData": "pymedplum.fhir.measure:MeasureSupplementalData",
    "Media": "pymedplum.fhir.media:Media",
    "Medication": "pymedplum.fhir.medication:Medication",
    "MedicationAdministration": "pymedplum.fhir.medicationadministration:MedicationAdministration",
    "MedicationAdministrationDosage": "pymedplum.fhir.medicationadministration:MedicationAdministrationDosage",
    "MedicationAdministrationPerformer": "pymedplum.fhir.medicationadministration:MedicationAdministrationPerformer",
    "MedicationBatch": "pymedplum.fhir.medication:MedicationBatch",
    "MedicationDispense": "pymedplum.fhir.medicationdispense:MedicationDispense",
    "MedicationDispensePerformer": "pymedplum.fhir.medicationdispense:MedicationDispensePerformer",
    "MedicationDispenseSubstitution": "pymedplum.fhir.medicationdispense:MedicationDispenseSubstitution",
    "MedicationIngredient": "pymedplum.fhir.medication:MedicationIngredient",
    "MedicationKnowledge": "pymedplum.fhir.medicationknowledge:MedicationKnowledge",
    "MedicationKnowledgeAdministrationGuidelines": "pymedplum.fhir.medicationknowledge:MedicationKnowledgeAdministrationGuidelines",
    "MedicationKnowledgeAdministrationGuidelinesDosage": "pymedplum.fhir.medicationknowledge:MedicationKnowledgeAdministrationGuidelinesDosage",
    "MedicationKnowledgeAdministrationGuidelinesPatientCharacteristics": "pymedplum.fhir.medicationknowledge:MedicationKnowledgeAdministrationGuidelinesPatientCharacteristics",
    "MedicationKnowledgeCost": "pymedplum.fhir.medicationknowledge:MedicationKnowledgeCost",
    "MedicationKnowledgeDrugCharacteristic": "pymedplum.fhir.medicationknowledge:MedicationKnowledgeDrugCharacteristic",
    "MedicationKnowledgeIngredient": "pymedplum.fhir.medicationknowledge:MedicationKnowledgeIngredient",
    "MedicationKnowledgeKinetics": "pymedplum.fhir.medicationknowledge:MedicationKnowledgeKinetics",
    "MedicationKnowledgeMedicineClassification": "pymedplum.fhir.medicationknowledge:MedicationKnowledgeMedicineClassification",
    "MedicationKnowledgeMonitoringProgram": "pymedplum.fhir.medicationknowledge:MedicationKnowledgeMonitoringProgram",
    "MedicationKnowledgeMonograph": "pymedplum.fhir.medicationknowledge:MedicationKnowledgeMonograph",
    "MedicationKnowledgePackaging": "pymedplum.fhir.medicationknowledge:MedicationKnowledgePackaging",
    "MedicationKnowledgeRegulatory": "pymedplum.fhir.medicationknowledge:MedicationKnowledgeRegulatory",
    "MedicationKnowledgeRegulatoryMaxDispense": "pymedplum.fhir.medicationknowledge:MedicationKnowledgeRegulatoryMaxDispense",
    "MedicationKnowledgeRegulatorySchedule": "pymedplum.fhir.medicationknowledge:MedicationKnowledgeRegulatorySchedule",
    "MedicationKnowledgeRegulatorySubstitution": "pymedplum.fhir.medicationknowledge:MedicationKnowledgeRegulatorySubstitution",
    "MedicationKnowledgeRelatedMedicationKnowledge": "pymedplum.fhir.medicationknowledge:MedicationKnowledgeRelatedMedicationKnowledge",
    "MedicationRequest": "pymedplum.fhir.medicationrequest:MedicationRequest",
    "MedicationRequestDispenseRequest": "pymedplum.fhir.medicationrequest:MedicationRequestDispenseRequest",
    "MedicationRequestDispenseRequestInitialFill": "pymedplum.fhir.medicationrequest:MedicationRequestDispenseRequestInitialFill",
    "MedicationRequestSubstitution": "pymedplum.fhir.medicationrequest:MedicationRequestSubstitution",
    "MedicationStatement": "pymedplum.fhir.medicationstatement:MedicationStatement",
    "MedicinalProduct": "pymedplum.fhir.medicinalproduct:MedicinalProduct",
    "MedicinalProductAuthorization": "pymedplum.fhir.medicinalproductauthorization:MedicinalProductAuthorization",
    "MedicinalProductAuthorizationJurisdictionalAuthorization": "pymedplum.fhir.medicinalproductauthorization:MedicinalProductAuthorizationJurisdictionalAuthorization",
    "MedicinalProductAuthorizationProcedure": "pymedplum.fhir.medicinalproductauthorization:MedicinalProductAuthorizationProcedure",
    "MedicinalProductContraindication": "pymedplum.fhir.medicinalproductcontraindication:MedicinalProductContraindication",
    "MedicinalProductContraindicationOtherTherapy": "pymedplum.fhir.medicinalproductcontraindication:MedicinalProductContraindicationOtherTherapy",
    "MedicinalProductIndication": "pymedplum.fhir.medicinalproductindication:MedicinalProductIndication",
    "MedicinalProductIndicationOtherTherapy": "pymedplum.fhir.medicinalproductindication:MedicinalProductIndicationOtherTherapy",
    "MedicinalProductIngredient": "pymedplum.fhir.medicinalproductingredient:MedicinalProductIngredient",
    "MedicinalProductIngredientSpecifiedSubstance": "pymedplum.fhir.medicinalproductingredient:MedicinalProductIngredientSpecifiedSubstance",
    "MedicinalProductIngredientSpecifiedSubstanceStrength": "pymedplum.fhir.medicinalproductingredient:MedicinalProductIngredientSpecifiedSubstanceStrength",
    "MedicinalProductIngredientSpecifiedSubstanceStrengthReferenceStrength": "pymedplum.fhir.medicinalproductingredient:MedicinalProductIngredientSpecifiedSubstanceStrengthReferenceStrength",
    "MedicinalProductIngredientSubstance": "pymedplum.fhir.medicinalproductingredient:MedicinalProductIngredientSubstance",
    "MedicinalProductInteraction": "pymedplum.fhir.medicinalproductinteraction:MedicinalProductInteraction",
    "MedicinalProductInteractionInteractant": "pymedplum.fhir.medicinalproductinteraction:MedicinalProductInteractionInteractant",
    "MedicinalProductManufactured": "pymedplum.fhir.medicinalproductmanufactured:MedicinalProductManufactured",
    "MedicinalProductManufacturingBusinessOperation": "pymedplum.fhir.medicinalproduct:MedicinalProductManufacturingBusinessOperation",
    "MedicinalProductName": "pymedplum.fhir.medicinalproduct:MedicinalProductName",
    "MedicinalProductNameCountryLanguage": "pymedplum.fhir.medicinalproduct:MedicinalProductNameCountryLanguage",
    "MedicinalProductNameNamePart": "pymedplum.fhir.medicinalproduct:MedicinalProductNameNamePart",
    "MedicinalProductPackaged": "pymedplum.fhir.medicinalproductpackaged:MedicinalProductPackaged",
    "MedicinalProductPackagedBatchIdentifier": "pymedplum.fhir.medicinalproductpackaged:MedicinalProductPackagedBatchIdentifier",
    "MedicinalProductPackagedPackageItem": "pymedplum.fhir.medicinalproductpackaged:MedicinalProductPackagedPackageItem",
    "MedicinalProductPharmaceutical": "pymedplum.fhir.medicinalproductpharmaceutical:MedicinalProductPharmaceutical",
    "MedicinalProductPharmaceuticalCharacteristics": "pymedplum.fhir.medicinalproductpharmaceutical:MedicinalProductPharmaceuticalCharacteristics",
    "MedicinalProductPharmaceuticalRouteOfAdministration": "pymedplum.fhir.medicinalproductpharmaceutical:MedicinalProductPharmaceuticalRouteOfAdministration",
    "MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpecies": "pymedplum.fhir.medicinalproductpharmaceutical:MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpecies",
    "MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpeciesWithdrawalPeriod": "pymedplum.fhir.medicinalproductpharmaceutical:MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpeciesWithdrawalPeriod",
    "MedicinalProductSpecialDesignation": "pymedplum.fhir.medicinalproduct:MedicinalProductSpecialDesignation",
    "MedicinalProductUndesirableEffect": "pymedplum.fhir.medicinalproductundesirableeffect:MedicinalProductUndesirableEffect",
    "MessageDefinition": "pymedplum.fhir.messagedefinition:MessageDefinition",
    "MessageDefinitionAllowedResponse": "pymedplum.fhir.messagedefinition:MessageDefinitionAllowedResponse",
    "MessageDefinitionFocus": "pymedplum.fhir.messagedefinition:MessageDefinitionFocus",
    "MessageHeader": "pymedplum.fhir.messageheader:MessageHeader",
    "MessageHeaderDestination": "pymedplum.fhir.messageheader:MessageHeaderDestination",
    "MessageHeaderResponse": "pymedplum.fhir.messageheader:MessageHeaderResponse",
    "MessageHeaderSource": "pymedplum.fhir.messageheader:MessageHeaderSource",
    "Meta": "pymedplum.fhir.meta:Meta",
    "MetadataResource": "pymedplum.fhir.metadataresource:MetadataResource",
    "MolecularSequence": "pymedplum.fhir.molecularsequence:MolecularSequence",
    "MolecularSequenceQuality": "pymedplum.fhir.molecularsequence:MolecularSequenceQuality",
    "MolecularSequenceQualityRoc": "pymedplum.fhir.molecularsequence:MolecularSequenceQualityRoc",
    "MolecularSequenceReferenceSeq": "pymedplum.fhir.molecularsequence:MolecularSequenceReferenceSeq",
    "MolecularSequenceRepository": "pymedplum.fhir.molecularsequence:MolecularSequenceRepository",
    "MolecularSequenceStructureVariant": "pymedplum.fhir.molecularsequence:MolecularSequenceStructureVariant",
    "MolecularSequenceStructureVariantInner": "pymedplum.fhir.molecularsequence:MolecularSequenceStructureVariantInner",
    "MolecularSequenceStructureVariantOuter": "pymedplum.fhir.molecularsequence:MolecularSequenceStructureVariantOuter",
    "MolecularSequenceVariant": "pymedplum.fhir.molecularsequence:MolecularSequenceVariant",
    "Money": "pymedplum.fhir.money:Money",
    "MoneyQuantity": "pymedplum.fhir.moneyquantity:MoneyQuantity",
    "NamingSystem": "pymedplum.fhir.namingsystem:NamingSystem",
    "NamingSystemUniqueId": "pymedplum.fhir.namingsystem:NamingSystemUniqueId",
    "Narrative": "pymedplum.fhir.narrative:Narrative",
    "NutritionOrder": "pymedplum.fhir.nutritionorder:NutritionOrder",
    "NutritionOrderEnteralFormula": "pymedplum.fhir.nutritionorder:NutritionOrderEnteralFormula",
    "NutritionOrderEnteralFormulaAdministration": "pymedplum.fhir.nutritionorder:NutritionOrderEnteralFormulaAdministration",
    "NutritionOrderOralDiet": "pymedplum.fhir.nutritionorder:NutritionOrderOralDiet",
    "NutritionOrderOralDietNutrient": "pymedplum.fhir.nutritionorder:NutritionOrderOralDietNutrient",
    "NutritionOrderOralDietTexture": "pymedplum.fhir.nutritionorder:NutritionOrderOralDietTexture",
    "NutritionOrderSupplement": "pymedplum.fhir.nutritionorder:NutritionOrderSupplement",
    "Observation": "pymedplum.fhir.observation:Observation",
    "ObservationComponent": "pymedplum.fhir.observation:ObservationComponent",
    "ObservationDefinition": "pymedplum.fhir.observationdefinition:ObservationDefinition",
    "ObservationDefinitionQualifiedInterval": "pymedplum.fhir.observationdefinition:ObservationDefinitionQualifiedInterval",
    "ObservationDefinitionQuantitativeDetails": "pymedplum.fhir.observationdefinition:ObservationDefinitionQuantitativeDetails",
    "ObservationReferenceRange": "pymedplum.fhir.observation:ObservationReferenceRange",
    "OperationDefinition": "pymedplum.fhir.operationdefinition:OperationDefinition",
    "OperationDefinitionOverload": "pymedplum.fhir.operationdefinition:OperationDefinitionOverload",
    "OperationDefinitionParameter": "pymedplum.fhir.operationdefinition:OperationDefinitionParameter",
    "OperationDefinitionParameterBinding": "pymedplum.fhir.operationdefinition:OperationDefinitionParameterBinding",
    "OperationDefinitionParameterReferencedFrom": "pymedplum.fhir.operationdefinition:OperationDefinitionParameterReferencedFrom",
    "OperationOutcome": "pymedplum.fhir.operationoutcome:OperationOutcome",
    "OperationOutcomeIssue": "pymedplum.fhir.operationoutcome:OperationOutcomeIssue",
    "Organization": "pymedplum.fhir.organization:Organization",
    "OrganizationAffiliation": "pymedplum.fhir.organizationaffiliation:OrganizationAffiliation",
    "OrganizationContact": "pymedplum.fhir.organization:OrganizationContact",
    "ParameterDefinition": "pymedplum.fhir.parameterdefinition:ParameterDefinition",
    "Parameters": "pymedplum.fhir.parameters:Parameters",
    "ParametersParameter": "pymedplum.fhir.parameters:ParametersParameter",
    "PasswordChangeRequest": "pymedplum.fhir.passwordchangerequest:PasswordChangeRequest",
    "Patient": "pymedplum.fhir.patient:Patient",
    "PatientCommunication": "pymedplum.fhir.patient:PatientCommunication",
    "PatientContact": "pymedplum.fhir.patient:PatientContact",
    "PatientLink": "pymedplum.fhir.patient:PatientLink",
    "PaymentNotice": "pymedplum.fhir.paymentnotice:PaymentNotice",
    "PaymentReconciliation": "pymedplum.fhir.paymentreconciliation:PaymentReconciliation",
    "PaymentReconciliationDetail": "pymedplum.fhir.paymentreconciliation:PaymentReconciliationDetail",
    "PaymentReconciliationProcessNote": "pymedplum.fhir.paymentreconciliation:PaymentReconciliationProcessNote",
    "Period": "pymedplum.fhir.period:Period",
    "Person": "pymedplum.fhir.person:Person",
    "PersonLink": "pymedplum.fhir.person:PersonLink",
    "PlanDefinition": "pymedplum.fhir.plandefinition:PlanDefinition",
    "PlanDefinitionAction": "pymedplum.fhir.plandefinition:PlanDefinitionAction",
    "PlanDefinitionActionCondition": "pymedplum.fhir.plandefinition:PlanDefinitionActionCondition",
    "PlanDefinitionActionDynamicValue": "pymedplum.fhir.plandefinition:PlanDefinitionActionDynamicValue",
    "PlanDefinitionActionParticipant": "pymedplum.fhir.plandefinition:PlanDefinitionActionParticipant",
    "PlanDefinitionActionRelatedAction": "pymedplum.fhir.plandefinition:PlanDefinitionActionRelatedAction",
    "PlanDefinitionGoal": "pymedplum.fhir.plandefinition:PlanDefinitionGoal",
    "PlanDefinitionGoalTarget": "pymedplum.fhir.plandefinition:PlanDefinitionGoalTarget",
    "Population": "pymedplum.fhir.population:Population",
    "Practitioner": "pymedplum.fhir.practitioner:Practitioner",
    "PractitionerQualification": "pymedplum.fhir.practitioner:PractitionerQualification",
    "PractitionerRole": "pymedplum.fhir.practitionerrole:PractitionerRole",
    "PractitionerRoleAvailableTime": "pymedplum.fhir.practitionerrole:PractitionerRoleAvailableTime",
    "PractitionerRoleNotAvailable": "pymedplum.fhir.practitionerrole:PractitionerRoleNotAvailable",
    "Procedure": "pymedplum.fhir.procedure:Procedure",
    "ProcedureFocalDevice": "pymedplum.fhir.procedure:ProcedureFocalDevice",
    "ProcedurePerformer": "pymedplum.fhir.procedure:ProcedurePerformer",
    "ProdCharacteristic": "pymedplum.fhir.prodcharacteristic:ProdCharacteristic",
    "ProductShelfLife": "pymedplum.fhir.productshelflife:ProductShelfLife",
    "Project": "pymedplum.fhir.project:Project",
    "ProjectDefaultProfile": "pymedplum.fhir.project:ProjectDefaultProfile",
    "ProjectLink": "pymedplum.fhir.project:ProjectLink",
    "ProjectMembership": "pymedplum.fhir.projectmembership:ProjectMembership",
    "ProjectMembershipAccess": "pymedplum.fhir.projectmembership:ProjectMembershipAccess",
    "ProjectMembershipAccessParameter": "pymedplum.fhir.projectmembership:ProjectMembershipAccessParameter",
    "ProjectSetting": "pymedplum.fhir.project:ProjectSetting",
    "ProjectSite": "pymedplum.fhir.project:ProjectSite",
    "Provenance": "pymedplum.fhir.provenance:Provenance",
    "ProvenanceAgent": "pymedplum.fhir.provenance:ProvenanceAgent",
    "ProvenanceEntity": "pymedplum.fhir.provenance:ProvenanceEntity",
    "Quantity": "pymedplum.fhir.quantity:Quantity",
    "Questionnaire": "pymedplum.fhir.questionnaire:Questionnaire",
    "QuestionnaireItem": "pymedplum.fhir.questionnaire:QuestionnaireItem",
    "QuestionnaireItemAnswerOption": "pymedplum.fhir.questionnaire:QuestionnaireItemAnswerOption",
    "QuestionnaireItemEnableWhen": "pymedplum.fhir.questionnaire:QuestionnaireItemEnableWhen",
    "QuestionnaireItemInitial": "pymedplum.fhir.questionnaire:QuestionnaireItemInitial",
    "QuestionnaireResponse": "pymedplum.fhir.questionnaireresponse:QuestionnaireResponse",
    "QuestionnaireResponseItem": "pymedplum.fhir.questionnaireresponse:QuestionnaireResponseItem",
    "QuestionnaireResponseItemAnswer": "pymedplum.fhir.questionnaireresponse:QuestionnaireResponseItemAnswer",
    "Range": "pymedplum.fhir.range:Range",
    "Ratio": "pymedplum.fhir.ratio:Ratio",
    "Reference": "pymedplum.fhir.reference:Reference",
    "RelatedArtifact": "pymedplum.fhir.relatedartifact:RelatedArtifact",
    "RelatedPerson": "pymedplum.fhir.relatedperson:RelatedPerson",
    "RelatedPersonCommunication": "pymedplum.fhir.relatedperson:RelatedPersonCommunication",
    "RequestGroup": "pymedplum.fhir.requestgroup:RequestGroup",
    "RequestGroupAction": "pymedplum.fhir.requestgroup:RequestGroupAction",
    "RequestGroupActionCondition": "pymedplum.fhir.requestgroup:RequestGroupActionCondition",
    "RequestGroupActionRelatedAction": "pymedplum.fhir.requestgroup:RequestGroupActionRelatedAction",
    "ResearchDefinition": "pymedplum.fhir.researchdefinition:ResearchDefinition",
    "ResearchElementDefinition": "pymedplum.fhir.researchelementdefinition:ResearchElementDefinition",
    "ResearchElementDefinitionCharacteristic": "pymedplum.fhir.researchelementdefinition:ResearchElementDefinitionCharacteristic",
    "ResearchStudy": "pymedplum.fhir.researchstudy:ResearchStudy",
    "ResearchStudyArm": "pymedplum.fhir.researchstudy:ResearchStudyArm",
    "ResearchStudyAssociatedParty": "pymedplum.fhir.researchstudy:ResearchStudyAssociatedParty",
    "ResearchStudyComparisonGroup": "pymedplum.fhir.researchstudy:ResearchStudyComparisonGroup",
    "ResearchStudyLabel": "pymedplum.fhir.researchstudy:ResearchStudyLabel",
    "ResearchStudyObjective": "pymedplum.fhir.researchstudy:ResearchStudyObjective",
    "ResearchStudyOutcomeMeasure": "pymedplum.fhir.researchstudy:ResearchStudyOutcomeMeasure",
    "ResearchStudyProgressStatus": "pymedplum.fhir.researchstudy:ResearchStudyProgressStatus",
    "ResearchStudyRecruitment": "pymedplum.fhir.researchstudy:ResearchStudyRecruitment",
    "ResearchSubject": "pymedplum.fhir.researchsubject:ResearchSubject",
    "RiskAssessment": "pymedplum.fhir.riskassessment:RiskAssessment",
    "RiskAssessmentPrediction": "pymedplum.fhir.riskassessment:RiskAssessmentPrediction",
    "RiskEvidenceSynthesis": "pymedplum.fhir.riskevidencesynthesis:RiskEvidenceSynthesis",
    "RiskEvidenceSynthesisCertainty": "pymedplum.fhir.riskevidencesynthesis:RiskEvidenceSynthesisCertainty",
    "RiskEvidenceSynthesisCertaintyCertaintySubcomponent": "pymedplum.fhir.riskevidencesynthesis:RiskEvidenceSynthesisCertaintyCertaintySubcomponent",
    "RiskEvidenceSynthesisRiskEstimate": "pymedplum.fhir.riskevidencesynthesis:RiskEvidenceSynthesisRiskEstimate",
    "RiskEvidenceSynthesisRiskEstimatePrecisionEstimate": "pymedplum.fhir.riskevidencesynthesis:RiskEvidenceSynthesisRiskEstimatePrecisionEstimate",
    "RiskEvidenceSynthesisSampleSize": "pymedplum.fhir.riskevidencesynthesis:RiskEvidenceSynthesisSampleSize",
    "SampledData": "pymedplum.fhir.sampleddata:SampledData",
    "Schedule": "pymedplum.fhir.schedule:Schedule",
    "SearchParameter": "pymedplum.fhir.searchparameter:SearchParameter",
    "SearchParameterComponent": "pymedplum.fhir.searchparameter:SearchParameterComponent",
    "ServiceRequest": "pymedplum.fhir.servicerequest:ServiceRequest",
    "Signature": "pymedplum.fhir.signature:Signature",
    "SimpleQuantity": "pymedplum.fhir.simplequantity:SimpleQuantity",
    "Slot": "pymedplum.fhir.slot:Slot",
    "SmartAppLaunch": "pymedplum.fhir.smartapplaunch:SmartAppLaunch",
    "Specimen": "pymedplum.fhir.specimen:Specimen",
    "SpecimenCollection": "pymedplum.fhir.specimen:SpecimenCollection",
    "SpecimenContainer": "pymedplum.fhir.specimen:SpecimenContainer",
    "SpecimenDefinition": "pymedplum.fhir.specimendefinition:SpecimenDefinition",
    "SpecimenDefinitionTypeTested": "pymedplum.fhir.specimendefinition:SpecimenDefinitionTypeTested",
    "SpecimenDefinitionTypeTestedContainer": "pymedplum.fhir.specimendefinition:SpecimenDefinitionTypeTestedContainer",
    "SpecimenDefinitionTypeTestedContainerAdditive": "pymedplum.fhir.specimendefinition:SpecimenDefinitionTypeTestedContainerAdditive",
    "SpecimenDefinitionTypeTestedHandling": "pymedplum.fhir.specimendefinition:SpecimenDefinitionTypeTestedHandling",
    "SpecimenProcessing": "pymedplum.fhir.specimen:SpecimenProcessing",
    "StructureDefinition": "pymedplum.fhir.structuredefinition:StructureDefinition",
    "StructureDefinitionContext": "pymedplum.fhir.structuredefinition:StructureDefinitionContext",
    "StructureDefinitionDifferential": "pymedplum.fhir.structuredefinition:StructureDefinitionDifferential",
    "StructureDefinitionMapping": "pymedplum.fhir.structuredefinition:StructureDefinitionMapping",
    "StructureDefinitionSnapshot": "pymedplum.fhir.structuredefinition:StructureDefinitionSnapshot",
    "StructureMap": "pymedplum.fhir.structuremap:StructureMap",
    "StructureMapGroup": "pymedplum.fhir.structuremap:StructureMapGroup",
    "StructureMapGroupInput": "pymedplum.fhir.structuremap:StructureMapGroupInput",
    "StructureMapGroupRule": "pymedplum.fhir.structuremap:StructureMapGroupRule",
    "StructureMapGroupRuleDependent": "pymedplum.fhir.structuremap:StructureMapGroupRuleDependent",
    "StructureMapGroupRuleSource": "pymedplum.fhir.structuremap:StructureMapGroupRuleSource",
    "StructureMapGroupRuleTarget": "pymedplum.fhir.structuremap:StructureMapGroupRuleTarget",
    "StructureMapGroupRuleTargetParameter": "pymedplum.fhir.structuremap:StructureMapGroupRuleTargetParameter",
    "StructureMapStructure": "pymedplum.fhir.structuremap:StructureMapStructure",
    "Subscription": "pymedplum.fhir.subscription:Subscription",
    "SubscriptionChannel": "pymedplum.fhir.subscription:SubscriptionChannel",
    "SubscriptionStatus": "pymedplum.fhir.subscriptionstatus:SubscriptionStatus",
    "SubscriptionStatusNotificationEvent": "pymedplum.fhir.subscriptionstatus:SubscriptionStatusNotificationEvent",
    "Substance": "pymedplum.fhir.substance:Substance",
    "SubstanceAmount": "pymedplum.fhir.substanceamount:SubstanceAmount",
    "SubstanceAmountReferenceRange": "pymedplum.fhir.substanceamount:SubstanceAmountReferenceRange",
    "SubstanceIngredient": "pymedplum.fhir.substance:SubstanceIngredient",
    "SubstanceInstance": "pymedplum.fhir.substance:SubstanceInstance",
    "SubstanceNucleicAcid": "pymedplum.fhir.substancenucleicacid:SubstanceNucleicAcid",
    "SubstanceNucleicAcidSubunit": "pymedplum.fhir.substancenucleicacid:SubstanceNucleicAcidSubunit",
    "SubstanceNucleicAcidSubunitLinkage": "pymedplum.fhir.substancenucleicacid:SubstanceNucleicAcidSubunitLinkage",
    "SubstanceNucleicAcidSubunitSugar": "pymedplum.fhir.substancenucleicacid:SubstanceNucleicAcidSubunitSugar",
    "SubstancePolymer": "pymedplum.fhir.substancepolymer:SubstancePolymer",
    "SubstancePolymerMonomerSet": "pymedplum.fhir.substancepolymer:SubstancePolymerMonomerSet",
    "SubstancePolymerMonomerSetStartingMaterial": "pymedplum.fhir.substancepolymer:SubstancePolymerMonomerSetStartingMaterial",
    "SubstancePolymerRepeat": "pymedplum.fhir.substancepolymer:SubstancePolymerRepeat",
    "SubstancePolymerRepeatRepeatUnit": "pymedplum.fhir.substancepolymer:SubstancePolymerRepeatRepeatUnit",
    "SubstancePolymerRepeatRepeatUnitDegreeOfPolymerisation": "pymedplum.fhir.substancepolymer:SubstancePolymerRepeatRepeatUnitDegreeOfPolymerisation",
    "SubstancePolymerRepeatRepeatUnitStructuralRepresentation": "pymedplum.fhir.substancepolymer:SubstancePolymerRepeatRepeatUnitStructuralRepresentation",
    "SubstanceProtein": "pymedplum.fhir.substanceprotein:SubstanceProtein",
    "SubstanceProteinSubunit": "pymedplum.fhir.substanceprotein:SubstanceProteinSubunit",
    "SubstanceReferenceInformation": "pymedplum.fhir.substancereferenceinformation:SubstanceReferenceInformation",
    "SubstanceReferenceInformationClassification": "pymedplum.fhir.substancereferenceinformation:SubstanceReferenceInformationClassification",
    "SubstanceReferenceInformationGene": "pymedplum.fhir.substancereferenceinformation:SubstanceReferenceInformationGene",
    "SubstanceReferenceInformationGeneElement": "pymedplum.fhir.substancereferenceinformation:SubstanceReferenceInformationGeneElement",
    "SubstanceReferenceInformationTarget": "pymedplum.fhir.substancereferenceinformation:SubstanceReferenceInformationTarget",
    "SubstanceSourceMaterial": "pymedplum.fhir.substancesourcematerial:SubstanceSourceMaterial",
    "SubstanceSourceMaterialFractionDescription": "pymedplum.fhir.substancesourcematerial:SubstanceSourceMaterialFractionDescription",
    "SubstanceSourceMaterialOrganism": "pymedplum.fhir.substancesourcematerial:SubstanceSourceMaterialOrganism",
    "SubstanceSourceMaterialOrganismAuthor": "pymedplum.fhir.substancesourcematerial:SubstanceSourceMaterialOrganismAuthor",
    "SubstanceSourceMaterialOrganismHybrid": "pymedplum.fhir.substancesourcematerial:SubstanceSourceMaterialOrganismHybrid",
    "SubstanceSourceMaterialOrganismOrganismGeneral": "pymedplum.fhir.substancesourcematerial:SubstanceSourceMaterialOrganismOrganismGeneral",
    "SubstanceSourceMaterialPartDescription": "pymedplum.fhir.substancesourcematerial:SubstanceSourceMaterialPartDescription",
    "SubstanceSpecification": "pymedplum.fhir.substancespecification:SubstanceSpecification",
    "SubstanceSpecificationCode": "pymedplum.fhir.substancespecification:SubstanceSpecificationCode",
    "SubstanceSpecificationMoiety": "pymedplum.fhir.substancespecification:SubstanceSpecificationMoiety",
    "SubstanceSpecificationName": "pymedplum.fhir.substancespecification:SubstanceSpecificationName",
    "SubstanceSpecificationNameOfficial": "pymedplum.fhir.substancespecification:SubstanceSpecificationNameOfficial",
    "SubstanceSpecificationProperty": "pymedplum.fhir.substancespecification:SubstanceSpecificationProperty",
    "SubstanceSpecificationRelationship": "pymedplum.fhir.substancespecification:SubstanceSpecificationRelationship",
    "SubstanceSpecificationStructure": "pymedplum.fhir.substancespecification:SubstanceSpecificationStructure",
    "SubstanceSpecificationStructureIsotope": "pymedplum.fhir.substancespecification:SubstanceSpecificationStructureIsotope",
    "SubstanceSpecificationStructureIsotopeMolecularWeight": "pymedplum.fhir.substancespecification:SubstanceSpecificationStructureIsotopeMolecularWeight",
    "SubstanceSpecificationStructureRepresentation": "pymedplum.fhir.substancespecification:SubstanceSpecificationStructureRepresentation",
    "SupplyDelivery": "pymedplum.fhir.supplydelivery:SupplyDelivery",
    "SupplyDeliverySuppliedItem": "pymedplum.fhir.supplydelivery:SupplyDeliverySuppliedItem",
    "SupplyRequest": "pymedplum.fhir.supplyrequest:SupplyRequest",
    "SupplyRequestParameter": "pymedplum.fhir.supplyrequest:SupplyRequestParameter",
    "Task": "pymedplum.fhir.task:Task",
    "TaskInput": "pymedplum.fhir.task:TaskInput",
    "TaskOutput": "pymedplum.fhir.task:TaskOutput",
    "TaskRestriction": "pymedplum.fhir.task:TaskRestriction",
    "TerminologyCapabilities": "pymedplum.fhir.terminologycapabilities:TerminologyCapabilities",
    "TerminologyCapabilitiesClosure": "pymedplum.fhir.terminologycapabilities:TerminologyCapabilitiesClosure",
    "TerminologyCapabilitiesCodeSystem": "pymedplum.fhir.terminologycapabilities:TerminologyCapabilitiesCodeSystem",
    "TerminologyCapabilitiesCodeSystemVersion": "pymedplum.fhir.terminologycapabilities:TerminologyCapabilitiesCodeSystemVersion",
    "TerminologyCapabilitiesCodeSystemVersionFilter": "pymedplum.fhir.terminologycapabilities:TerminologyCapabilitiesCodeSystemVersionFilter",
    "TerminologyCapabilitiesExpansion": "pymedplum.fhir.terminologycapabilities:TerminologyCapabilitiesExpansion",
    "TerminologyCapabilitiesExpansionParameter": "pymedplum.fhir.terminologycapabilities:TerminologyCapabilitiesExpansionParameter",
    "TerminologyCapabilitiesImplementation": "pymedplum.fhir.terminologycapabilities:TerminologyCapabilitiesImplementation",
    "TerminologyCapabilitiesSoftware": "pymedplum.fhir.terminologycapabilities:TerminologyCapabilitiesSoftware",
    "TerminologyCapabilitiesTranslation": "pymedplum.fhir.terminologycapabilities:TerminologyCapabilitiesTranslation",
    "TerminologyCapabilitiesValidateCode": "pymedplum.fhir.terminologycapabilities:TerminologyCapabilitiesValidateCode",
    "TestReport": "pymedplum.fhir.testreport:TestReport",
    "TestReportParticipant": "pymedplum.fhir.testreport:TestReportParticipant",
    "TestReportSetup": "pymedplum.fhir.testreport:TestReportSetup",
    "TestReportSetupAction": "pymedplum.fhir.testreport:TestReportSetupAction",
    "TestReportSetupActionAssert": "pymedplum.fhir.testreport:TestReportSetupActionAssert",
    "TestReportSetupActionOperation": "pymedplum.fhir.testreport:TestReportSetupActionOperation",
    "TestReportTeardown": "pymedplum.fhir.testreport:TestReportTeardown",
    "TestReportTeardownAction": "pymedplum.fhir.testreport:TestReportTeardownAction",
    "TestReportTest": "pymedplum.fhir.testreport:TestReportTest",
    "TestReportTestAction": "pymedplum.fhir.testreport:TestReportTestAction",
    "TestScript": "pymedplum.fhir.testscript:TestScript",
    "TestScriptDestination": "pymedplum.fhir.testscript:TestScriptDestination",
    "TestScriptFixture": "pymedplum.fhir.testscript:TestScriptFixture",
    "TestScriptMetadata": "pymedplum.fhir.testscript:TestScriptMetadata",
    "TestScriptMetadataCapability": "pymedplum.fhir.testscript:TestScriptMetadataCapability",
    "TestScriptMetadataLink": "pymedplum.fhir.testscript:TestScriptMetadataLink",
    "TestScriptOrigin": "pymedplum.fhir.testscript:TestScriptOrigin",
    "TestScriptSetup": "pymedplum.fhir.testscript:TestScriptSetup",
    "TestScriptSetupAction": "pymedplum.fhir.testscript:TestScriptSetupAction",
    "TestScriptSetupActionAssert": "pymedplum.fhir.testscript:TestScriptSetupActionAssert",
    "TestScriptSetupActionOperation": "pymedplum.fhir.testscript:TestScriptSetupActionOperation",
    "TestScriptSetupActionOperationRequestHeader": "pymedplum.fhir.testscript:TestScriptSetupActionOperationRequestHeader",
    "TestScriptTeardown": "pymedplum.fhir.testscript:TestScriptTeardown",
    "TestScriptTeardownAction": "pymedplum.fhir.testscript:TestScriptTeardownAction",
    "TestScriptTest": "pymedplum.fhir.testscript:TestScriptTest",
    "TestScriptTestAction": "pymedplum.fhir.testscript:TestScriptTestAction",
    "TestScriptVariable": "pymedplum.fhir.testscript:TestScriptVariable",
    "Timing": "pymedplum.fhir.timing:Timing",
    "TimingRepeat": "pymedplum.fhir.timing:TimingRepeat",
    "TriggerDefinition": "pymedplum.fhir.triggerdefinition:TriggerDefinition",
    "UsageContext": "pymedplum.fhir.usagecontext:UsageContext",
    "User": "pymedplum.fhir.user:User",
    "UserConfiguration": "pymedplum.fhir.userconfiguration:UserConfiguration",
    "UserConfigurationMenu": "pymedplum.fhir.userconfiguration:UserConfigurationMenu",
    "UserConfigurationMenuLink": "pymedplum.fhir.userconfiguration:UserConfigurationMenuLink",
    "UserConfigurationOption": "pymedplum.fhir.userconfiguration:UserConfigurationOption",
    "UserConfigurationSearch": "pymedplum.fhir.userconfiguration:UserConfigurationSearch",
    "UserSecurityRequest": "pymedplum.fhir.usersecurityrequest:UserSecurityRequest",
    "ValueSet": "pymedplum.fhir.valueset:ValueSet",
    "ValueSetCompose": "pymedplum.fhir.valueset:ValueSetCompose",
    "ValueSetComposeInclude": "pymedplum.fhir.valueset:ValueSetComposeInclude",
    "ValueSetComposeIncludeConcept": "pymedplum.fhir.valueset:ValueSetComposeIncludeConcept",
    "ValueSetComposeIncludeConceptDesignation": "pymedplum.fhir.valueset:ValueSetComposeIncludeConceptDesignation",
    "ValueSetComposeIncludeFilter": "pymedplum.fhir.valueset:ValueSetComposeIncludeFilter",
    "ValueSetExpansion": "pymedplum.fhir.valueset:ValueSetExpansion",
    "ValueSetExpansionContains": "pymedplum.fhir.valueset:ValueSetExpansionContains",
    "ValueSetExpansionParameter": "pymedplum.fhir.valueset:ValueSetExpansionParameter",
    "VerificationResult": "pymedplum.fhir.verificationresult:VerificationResult",
    "VerificationResultAttestation": "pymedplum.fhir.verificationresult:VerificationResultAttestation",
    "VerificationResultPrimarySource": "pymedplum.fhir.verificationresult:VerificationResultPrimarySource",
    "VerificationResultValidator": "pymedplum.fhir.verificationresult:VerificationResultValidator",
    "ViewDefinition": "pymedplum.fhir.viewdefinition:ViewDefinition",
    "ViewDefinitionConstant": "pymedplum.fhir.viewdefinition:ViewDefinitionConstant",
    "ViewDefinitionSelect": "pymedplum.fhir.viewdefinition:ViewDefinitionSelect",
    "ViewDefinitionSelectColumn": "pymedplum.fhir.viewdefinition:ViewDefinitionSelectColumn",
    "ViewDefinitionSelectColumnTag": "pymedplum.fhir.viewdefinition:ViewDefinitionSelectColumnTag",
    "ViewDefinitionWhere": "pymedplum.fhir.viewdefinition:ViewDefinitionWhere",
    "VisionPrescription": "pymedplum.fhir.visionprescription:VisionPrescription",
    "VisionPrescriptionLensSpecification": "pymedplum.fhir.visionprescription:VisionPrescriptionLensSpecification",
    "VisionPrescriptionLensSpecificationPrism": "pymedplum.fhir.visionprescription:VisionPrescriptionLensSpecificationPrism",
}


# ============================================================================
# Introspection Support
# ============================================================================


def __dir__() -> list[str]:
    """Return all available resource names for IDE autocompletion.

    IDEs use this to populate autocomplete suggestions. We return:
    - All registered resource names (REGISTRY.keys())
    - Already-cached imports (globals())
    """
    return sorted(
        set(
            list(REGISTRY.keys())  # All available resources
            + list(globals().keys())  # Already-cached imports
        )
    )


# Type names to skip during dependency extraction
_TYPING_SKIP = {
    "Optional",
    "Union",
    "List",
    "Dict",
    "Any",
    "Literal",
    "Type",
    "ForwardRef",
    "Annotated",
    "Callable",
    "Tuple",
    "Set",
    "ResourceType",  # TypeScript type alias, not a real Python class
}


def _get_model_lock(name: str) -> threading.RLock:
    """Get or create a per-model lock to serialize loading of the same model.

    This prevents multiple threads from simultaneously importing the same model,
    which could cause import-time state corruption.
    """
    with _MODEL_LOCKS_LOCK:
        if name not in _MODEL_LOCKS:
            _MODEL_LOCKS[name] = threading.RLock()
        return _MODEL_LOCKS[name]


# ============================================================================
# Dependency Resolution
# ============================================================================


def _extract_referenced_types(model_class: type[MedplumFHIRBase]) -> set[str]:
    """Extract all type references from a model including parent classes via MRO.

    No locks needed here as we're only reading class annotations.
    """
    out: set[str] = set()
    try:
        for base_class in model_class.__mro__:
            if (
                base_class is object
                or not hasattr(base_class, "__annotations__")
                or not hasattr(base_class, "__module__")
                or not base_class.__module__.startswith("pymedplum.fhir")
            ):
                continue

            for ann in base_class.__annotations__.values():
                for m in re.findall(r"\b([A-Z][a-zA-Z0-9_]*)\b", str(ann)):
                    if m in REGISTRY and m not in _TYPING_SKIP:
                        out.add(m)
    except Exception:
        pass
    return out


def _load_model_and_dependencies(
    name: str, visited: set[str] | None = None, newly_loaded: set[str] | None = None
) -> None:
    """Recursively load a model class and all its dependencies with per-model locking.

    Args:
        name: Name of the model to load
        visited: Set of already-visited models (prevents infinite recursion)
        newly_loaded: Set to track which models were loaded in this call
    """
    if visited is None:
        visited = set()
    if newly_loaded is None:
        newly_loaded = set()

    if name in visited or name not in REGISTRY:
        return

    # Detect circular dependencies
    with _LOADING_STACK_LOCK:
        if name in _LOADING_STACK:
            return  # Already being loaded by this or another thread
        _LOADING_STACK.add(name)

    try:
        # Acquire per-model lock to serialize loading of this specific model
        model_lock = _get_model_lock(name)
        with model_lock:
            visited.add(name)

            # Double-check within the lock: another thread may have loaded this while we waited
            if name in _TYPES_NS:
                return

            try:
                modpath, clsname = REGISTRY[name].split(":")
                mod = importlib.import_module(modpath)
                cls = getattr(mod, clsname)
            except Exception:
                return

            # Load safely under lock
            _TYPES_NS[name] = cls
            newly_loaded.add(name)

            # Load dependencies recursively
            for dep in _extract_referenced_types(cls):
                if dep not in _TYPES_NS:
                    _load_model_and_dependencies(dep, visited, newly_loaded)
    finally:
        with _LOADING_STACK_LOCK:
            _LOADING_STACK.discard(name)


# ============================================================================
# Base Class Preloading
# ============================================================================

_FHIR_BASE_CLASSES = [
    "Element",
    "Extension",
    "BackboneElement",
    "Meta",
    "Narrative",
    "Identifier",
    "HumanName",
    "Address",
    "ContactPoint",
    "CodeableConcept",
    "Coding",
    "Reference",
    "Period",
    "Quantity",
]
_BASE_CLASSES_LOADED = False
_BASE_CLASSES_LOCK = threading.Lock()


# ============================================================================
# Lazy Loading Entry Point
# ============================================================================


def __getattr__(name: str) -> Any:
    """Lazy load FHIR models on first access with proper thread synchronization.

    This implementation is safe for:
    - CPython with GIL (Python < 3.13)
    - CPython without GIL (Python 3.13+)
    - Other Python implementations (PyPy, Jython, etc.)

    Uses multiple layers of locking:
    1. Per-model locks: Prevent concurrent imports of the same model
    2. Rebuild lock: Serialize Pydantic model_rebuild() operations
    3. Base classes lock: Serialize one-time base class initialization
    """
    global _BASE_CLASSES_LOADED, _TYPES_NS_VERSION, _LAST_REBUILT_VERSION  # noqa: PLW0603

    if name.startswith("_"):
        raise AttributeError(name)
    if name not in REGISTRY:
        raise AttributeError(name)

    # First, check if already cached (fast path, no lock needed after first access)
    if name in _TYPES_NS:
        # Ensure it's in globals() for subsequent accesses
        if name not in globals():
            globals()[name] = _TYPES_NS[name]
        return _TYPES_NS[name]

    with _REBUILD_LOCK:
        # Re-check after acquiring lock (another thread may have loaded it)
        if name in _TYPES_NS:
            if name not in globals():
                globals()[name] = _TYPES_NS[name]
            return _TYPES_NS[name]

        newly_loaded: set[str] = set()

        # One-time initialization of base classes (serialized across all threads)
        if not _BASE_CLASSES_LOADED:
            with _BASE_CLASSES_LOCK:
                # Triple-check pattern: verify again after acquiring lock
                if not _BASE_CLASSES_LOADED:
                    for base_name in _FHIR_BASE_CLASSES:
                        if base_name in REGISTRY and base_name not in _TYPES_NS:
                            _load_model_and_dependencies(
                                base_name, newly_loaded=newly_loaded
                            )
                    _BASE_CLASSES_LOADED = True

        # Load requested class and its dependencies
        _load_model_and_dependencies(name, newly_loaded=newly_loaded)

        # Update version if new classes were loaded
        if newly_loaded:
            _TYPES_NS_VERSION += 1

        # Rebuild all loaded models when namespace changes
        # This is expensive but necessary for forward reference resolution
        if _LAST_REBUILT_VERSION != _TYPES_NS_VERSION:
            loaded_models = list(_TYPES_NS.values())
            for model in loaded_models:
                if hasattr(model, "model_rebuild"):
                    try:
                        model.model_rebuild(
                            _types_namespace=_TYPES_NS, raise_errors=True
                        )
                    except Exception as e:
                        import sys

                        print(
                            f"Warning: Failed to rebuild {model.__name__}: {e}",
                            file=sys.stderr,
                        )
            _LAST_REBUILT_VERSION = _TYPES_NS_VERSION

        obj = _TYPES_NS[name]
        globals()[name] = obj  # Cache to avoid future __getattr__ calls
        return obj


# ============================================================================
# Type Checking Support
# ============================================================================

if TYPE_CHECKING:
    # Type checkers get the full union for better inference.
    # These imports are ONLY used by type checkers, not at runtime.
    from pymedplum.fhir.accesspolicy import (
        AccessPolicy,
        AccessPolicyIpAccessRule,
        AccessPolicyResource,
    )
    from pymedplum.fhir.account import Account, AccountCoverage, AccountGuarantor
    from pymedplum.fhir.activitydefinition import (
        ActivityDefinition,
        ActivityDefinitionDynamicValue,
        ActivityDefinitionParticipant,
    )
    from pymedplum.fhir.address import Address
    from pymedplum.fhir.adverseevent import (
        AdverseEvent,
        AdverseEventSuspectEntity,
        AdverseEventSuspectEntityCausality,
    )
    from pymedplum.fhir.age import Age
    from pymedplum.fhir.agent import Agent, AgentChannel, AgentSetting
    from pymedplum.fhir.allergyintolerance import (
        AllergyIntolerance,
        AllergyIntoleranceReaction,
    )
    from pymedplum.fhir.annotation import Annotation
    from pymedplum.fhir.appointment import Appointment, AppointmentParticipant
    from pymedplum.fhir.appointmentresponse import AppointmentResponse
    from pymedplum.fhir.asyncjob import AsyncJob
    from pymedplum.fhir.attachment import Attachment
    from pymedplum.fhir.auditevent import (
        AuditEvent,
        AuditEventAgent,
        AuditEventAgentNetwork,
        AuditEventEntity,
        AuditEventEntityDetail,
        AuditEventSource,
    )
    from pymedplum.fhir.backboneelement import BackboneElement
    from pymedplum.fhir.basic import Basic
    from pymedplum.fhir.binary import Binary
    from pymedplum.fhir.biologicallyderivedproduct import (
        BiologicallyDerivedProduct,
        BiologicallyDerivedProductCollection,
        BiologicallyDerivedProductManipulation,
        BiologicallyDerivedProductProcessing,
        BiologicallyDerivedProductStorage,
    )
    from pymedplum.fhir.bodystructure import BodyStructure
    from pymedplum.fhir.bot import Bot
    from pymedplum.fhir.bulkdataexport import (
        BulkDataExport,
        BulkDataExportDeleted,
        BulkDataExportError,
        BulkDataExportOutput,
    )
    from pymedplum.fhir.bundle import (
        Bundle,
        BundleEntry,
        BundleEntryRequest,
        BundleEntryResponse,
        BundleEntrySearch,
        BundleLink,
    )
    from pymedplum.fhir.capabilitystatement import (
        CapabilityStatement,
        CapabilityStatementDocument,
        CapabilityStatementImplementation,
        CapabilityStatementMessaging,
        CapabilityStatementMessagingEndpoint,
        CapabilityStatementMessagingSupportedMessage,
        CapabilityStatementRest,
        CapabilityStatementRestInteraction,
        CapabilityStatementRestResource,
        CapabilityStatementRestResourceInteraction,
        CapabilityStatementRestResourceOperation,
        CapabilityStatementRestResourceSearchParam,
        CapabilityStatementRestSecurity,
        CapabilityStatementSoftware,
    )
    from pymedplum.fhir.careplan import (
        CarePlan,
        CarePlanActivity,
        CarePlanActivityDetail,
    )
    from pymedplum.fhir.careteam import CareTeam, CareTeamParticipant
    from pymedplum.fhir.catalogentry import CatalogEntry, CatalogEntryRelatedEntry
    from pymedplum.fhir.chargeitem import ChargeItem, ChargeItemPerformer
    from pymedplum.fhir.chargeitemdefinition import (
        ChargeItemDefinition,
        ChargeItemDefinitionApplicability,
        ChargeItemDefinitionPropertyGroup,
        ChargeItemDefinitionPropertyGroupPriceComponent,
    )
    from pymedplum.fhir.claim import (
        Claim,
        ClaimAccident,
        ClaimCareTeam,
        ClaimDiagnosis,
        ClaimInsurance,
        ClaimItem,
        ClaimItemDetail,
        ClaimItemDetailSubDetail,
        ClaimPayee,
        ClaimProcedure,
        ClaimRelated,
        ClaimSupportingInfo,
    )
    from pymedplum.fhir.claimresponse import (
        ClaimResponse,
        ClaimResponseAddItem,
        ClaimResponseAddItemDetail,
        ClaimResponseAddItemDetailSubDetail,
        ClaimResponseError,
        ClaimResponseInsurance,
        ClaimResponseItem,
        ClaimResponseItemAdjudication,
        ClaimResponseItemDetail,
        ClaimResponseItemDetailSubDetail,
        ClaimResponsePayment,
        ClaimResponseProcessNote,
        ClaimResponseTotal,
    )
    from pymedplum.fhir.clientapplication import (
        ClientApplication,
        ClientApplicationSignInForm,
    )
    from pymedplum.fhir.clinicalimpression import (
        ClinicalImpression,
        ClinicalImpressionFinding,
        ClinicalImpressionInvestigation,
    )
    from pymedplum.fhir.codeableconcept import CodeableConcept
    from pymedplum.fhir.codesystem import (
        CodeSystem,
        CodeSystemConcept,
        CodeSystemConceptDesignation,
        CodeSystemConceptProperty,
        CodeSystemFilter,
        CodeSystemProperty,
    )
    from pymedplum.fhir.coding import Coding
    from pymedplum.fhir.communication import Communication, CommunicationPayload
    from pymedplum.fhir.communicationrequest import (
        CommunicationRequest,
        CommunicationRequestPayload,
    )
    from pymedplum.fhir.compartmentdefinition import (
        CompartmentDefinition,
        CompartmentDefinitionResource,
    )
    from pymedplum.fhir.composition import (
        Composition,
        CompositionAttester,
        CompositionEvent,
        CompositionRelatesTo,
        CompositionSection,
    )
    from pymedplum.fhir.conceptmap import (
        ConceptMap,
        ConceptMapGroup,
        ConceptMapGroupElement,
        ConceptMapGroupElementTarget,
        ConceptMapGroupElementTargetDependsOn,
        ConceptMapGroupUnmapped,
    )
    from pymedplum.fhir.condition import Condition, ConditionEvidence, ConditionStage
    from pymedplum.fhir.consent import (
        Consent,
        ConsentPolicy,
        ConsentProvision,
        ConsentProvisionActor,
        ConsentProvisionData,
        ConsentVerification,
    )
    from pymedplum.fhir.contactdetail import ContactDetail
    from pymedplum.fhir.contactpoint import ContactPoint
    from pymedplum.fhir.contract import (
        Contract,
        ContractContentDefinition,
        ContractFriendly,
        ContractLegal,
        ContractRule,
        ContractSigner,
        ContractTerm,
        ContractTermAction,
        ContractTermActionSubject,
        ContractTermAsset,
        ContractTermAssetContext,
        ContractTermAssetValuedItem,
        ContractTermOffer,
        ContractTermOfferAnswer,
        ContractTermOfferParty,
        ContractTermSecurityLabel,
    )
    from pymedplum.fhir.contributor import Contributor
    from pymedplum.fhir.count import Count
    from pymedplum.fhir.coverage import (
        Coverage,
        CoverageClass,
        CoverageCostToBeneficiary,
        CoverageCostToBeneficiaryException,
    )
    from pymedplum.fhir.coverageeligibilityrequest import (
        CoverageEligibilityRequest,
        CoverageEligibilityRequestInsurance,
        CoverageEligibilityRequestItem,
        CoverageEligibilityRequestItemDiagnosis,
        CoverageEligibilityRequestSupportingInfo,
    )
    from pymedplum.fhir.coverageeligibilityresponse import (
        CoverageEligibilityResponse,
        CoverageEligibilityResponseError,
        CoverageEligibilityResponseInsurance,
        CoverageEligibilityResponseInsuranceItem,
        CoverageEligibilityResponseInsuranceItemBenefit,
    )
    from pymedplum.fhir.datarequirement import (
        DataRequirement,
        DataRequirementCodeFilter,
        DataRequirementDateFilter,
        DataRequirementSort,
    )
    from pymedplum.fhir.detectedissue import (
        DetectedIssue,
        DetectedIssueEvidence,
        DetectedIssueMitigation,
    )
    from pymedplum.fhir.device import (
        Device,
        DeviceDeviceName,
        DeviceProperty,
        DeviceSpecialization,
        DeviceUdiCarrier,
        DeviceVersion,
    )
    from pymedplum.fhir.devicedefinition import (
        DeviceDefinition,
        DeviceDefinitionCapability,
        DeviceDefinitionClassification,
        DeviceDefinitionDeviceName,
        DeviceDefinitionMaterial,
        DeviceDefinitionProperty,
        DeviceDefinitionSpecialization,
        DeviceDefinitionUdiDeviceIdentifier,
    )
    from pymedplum.fhir.devicemetric import DeviceMetric, DeviceMetricCalibration
    from pymedplum.fhir.devicerequest import DeviceRequest, DeviceRequestParameter
    from pymedplum.fhir.deviceusestatement import DeviceUseStatement
    from pymedplum.fhir.diagnosticreport import DiagnosticReport, DiagnosticReportMedia
    from pymedplum.fhir.distance import Distance
    from pymedplum.fhir.documentmanifest import (
        DocumentManifest,
        DocumentManifestRelated,
    )
    from pymedplum.fhir.documentreference import (
        DocumentReference,
        DocumentReferenceContent,
        DocumentReferenceContext,
        DocumentReferenceRelatesTo,
    )
    from pymedplum.fhir.domainconfiguration import DomainConfiguration
    from pymedplum.fhir.dosage import Dosage, DosageDoseAndRate
    from pymedplum.fhir.duration import Duration
    from pymedplum.fhir.effectevidencesynthesis import (
        EffectEvidenceSynthesis,
        EffectEvidenceSynthesisCertainty,
        EffectEvidenceSynthesisCertaintyCertaintySubcomponent,
        EffectEvidenceSynthesisEffectEstimate,
        EffectEvidenceSynthesisEffectEstimatePrecisionEstimate,
        EffectEvidenceSynthesisResultsByExposure,
        EffectEvidenceSynthesisSampleSize,
    )
    from pymedplum.fhir.element import Element
    from pymedplum.fhir.elementdefinition import (
        ElementDefinition,
        ElementDefinitionBase,
        ElementDefinitionBinding,
        ElementDefinitionConstraint,
        ElementDefinitionExample,
        ElementDefinitionMapping,
        ElementDefinitionSlicing,
        ElementDefinitionSlicingDiscriminator,
        ElementDefinitionType,
    )
    from pymedplum.fhir.encounter import (
        Encounter,
        EncounterClassHistory,
        EncounterDiagnosis,
        EncounterHospitalization,
        EncounterLocation,
        EncounterParticipant,
        EncounterStatusHistory,
    )
    from pymedplum.fhir.endpoint import Endpoint
    from pymedplum.fhir.enrollmentrequest import EnrollmentRequest
    from pymedplum.fhir.enrollmentresponse import EnrollmentResponse
    from pymedplum.fhir.episodeofcare import (
        EpisodeOfCare,
        EpisodeOfCareDiagnosis,
        EpisodeOfCareStatusHistory,
    )
    from pymedplum.fhir.eventdefinition import EventDefinition
    from pymedplum.fhir.evidence import Evidence
    from pymedplum.fhir.evidencevariable import (
        EvidenceVariable,
        EvidenceVariableCharacteristic,
        EvidenceVariableCharacteristicDefinitionByCombination,
        EvidenceVariableCharacteristicDefinitionByTypeAndValue,
        EvidenceVariableCharacteristicTimeFromEvent,
    )
    from pymedplum.fhir.examplescenario import (
        ExampleScenario,
        ExampleScenarioActor,
        ExampleScenarioInstance,
        ExampleScenarioInstanceContainedInstance,
        ExampleScenarioInstanceVersion,
        ExampleScenarioProcess,
        ExampleScenarioProcessStep,
        ExampleScenarioProcessStepAlternative,
        ExampleScenarioProcessStepOperation,
    )
    from pymedplum.fhir.explanationofbenefit import (
        ExplanationOfBenefit,
        ExplanationOfBenefitAccident,
        ExplanationOfBenefitAddItem,
        ExplanationOfBenefitAddItemDetail,
        ExplanationOfBenefitAddItemDetailSubDetail,
        ExplanationOfBenefitBenefitBalance,
        ExplanationOfBenefitBenefitBalanceFinancial,
        ExplanationOfBenefitCareTeam,
        ExplanationOfBenefitDiagnosis,
        ExplanationOfBenefitInsurance,
        ExplanationOfBenefitItem,
        ExplanationOfBenefitItemAdjudication,
        ExplanationOfBenefitItemDetail,
        ExplanationOfBenefitItemDetailSubDetail,
        ExplanationOfBenefitPayee,
        ExplanationOfBenefitPayment,
        ExplanationOfBenefitProcedure,
        ExplanationOfBenefitProcessNote,
        ExplanationOfBenefitRelated,
        ExplanationOfBenefitSupportingInfo,
        ExplanationOfBenefitTotal,
    )
    from pymedplum.fhir.expression import Expression
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.familymemberhistory import (
        FamilyMemberHistory,
        FamilyMemberHistoryCondition,
    )
    from pymedplum.fhir.flag import Flag
    from pymedplum.fhir.goal import Goal, GoalTarget
    from pymedplum.fhir.graphdefinition import (
        GraphDefinition,
        GraphDefinitionLink,
        GraphDefinitionLinkTarget,
        GraphDefinitionLinkTargetCompartment,
    )
    from pymedplum.fhir.group import Group, GroupCharacteristic, GroupMember
    from pymedplum.fhir.guidanceresponse import GuidanceResponse
    from pymedplum.fhir.healthcareservice import (
        HealthcareService,
        HealthcareServiceAvailableTime,
        HealthcareServiceEligibility,
        HealthcareServiceNotAvailable,
    )
    from pymedplum.fhir.humanname import HumanName
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.identityprovider import IdentityProvider
    from pymedplum.fhir.imagingstudy import (
        ImagingStudy,
        ImagingStudySeries,
        ImagingStudySeriesInstance,
        ImagingStudySeriesPerformer,
    )
    from pymedplum.fhir.immunization import (
        Immunization,
        ImmunizationEducation,
        ImmunizationPerformer,
        ImmunizationProtocolApplied,
        ImmunizationReaction,
    )
    from pymedplum.fhir.immunizationevaluation import ImmunizationEvaluation
    from pymedplum.fhir.immunizationrecommendation import (
        ImmunizationRecommendation,
        ImmunizationRecommendationRecommendation,
        ImmunizationRecommendationRecommendationDateCriterion,
    )
    from pymedplum.fhir.implementationguide import (
        ImplementationGuide,
        ImplementationGuideDefinition,
        ImplementationGuideDefinitionGrouping,
        ImplementationGuideDefinitionPage,
        ImplementationGuideDefinitionParameter,
        ImplementationGuideDefinitionResource,
        ImplementationGuideDefinitionTemplate,
        ImplementationGuideDependsOn,
        ImplementationGuideGlobal,
        ImplementationGuideManifest,
        ImplementationGuideManifestPage,
        ImplementationGuideManifestResource,
    )
    from pymedplum.fhir.insuranceplan import (
        InsurancePlan,
        InsurancePlanContact,
        InsurancePlanCoverage,
        InsurancePlanCoverageBenefit,
        InsurancePlanCoverageBenefitLimit,
        InsurancePlanPlan,
        InsurancePlanPlanGeneralCost,
        InsurancePlanPlanSpecificCost,
        InsurancePlanPlanSpecificCostBenefit,
        InsurancePlanPlanSpecificCostBenefitCost,
    )
    from pymedplum.fhir.invoice import (
        Invoice,
        InvoiceLineItem,
        InvoiceLineItemPriceComponent,
        InvoiceParticipant,
    )
    from pymedplum.fhir.jsonwebkey import JsonWebKey
    from pymedplum.fhir.library import Library
    from pymedplum.fhir.linkage import Linkage, LinkageItem
    from pymedplum.fhir.list import List, ListEntry
    from pymedplum.fhir.location import (
        Location,
        LocationHoursOfOperation,
        LocationPosition,
    )
    from pymedplum.fhir.login import Login
    from pymedplum.fhir.marketingstatus import MarketingStatus
    from pymedplum.fhir.measure import (
        Measure,
        MeasureGroup,
        MeasureGroupPopulation,
        MeasureGroupStratifier,
        MeasureGroupStratifierComponent,
        MeasureSupplementalData,
    )
    from pymedplum.fhir.measurereport import (
        MeasureReport,
        MeasureReportGroup,
        MeasureReportGroupPopulation,
        MeasureReportGroupStratifier,
        MeasureReportGroupStratifierStratum,
        MeasureReportGroupStratifierStratumComponent,
        MeasureReportGroupStratifierStratumPopulation,
    )
    from pymedplum.fhir.media import Media
    from pymedplum.fhir.medication import (
        Medication,
        MedicationBatch,
        MedicationIngredient,
    )
    from pymedplum.fhir.medicationadministration import (
        MedicationAdministration,
        MedicationAdministrationDosage,
        MedicationAdministrationPerformer,
    )
    from pymedplum.fhir.medicationdispense import (
        MedicationDispense,
        MedicationDispensePerformer,
        MedicationDispenseSubstitution,
    )
    from pymedplum.fhir.medicationknowledge import (
        MedicationKnowledge,
        MedicationKnowledgeAdministrationGuidelines,
        MedicationKnowledgeAdministrationGuidelinesDosage,
        MedicationKnowledgeAdministrationGuidelinesPatientCharacteristics,
        MedicationKnowledgeCost,
        MedicationKnowledgeDrugCharacteristic,
        MedicationKnowledgeIngredient,
        MedicationKnowledgeKinetics,
        MedicationKnowledgeMedicineClassification,
        MedicationKnowledgeMonitoringProgram,
        MedicationKnowledgeMonograph,
        MedicationKnowledgePackaging,
        MedicationKnowledgeRegulatory,
        MedicationKnowledgeRegulatoryMaxDispense,
        MedicationKnowledgeRegulatorySchedule,
        MedicationKnowledgeRegulatorySubstitution,
        MedicationKnowledgeRelatedMedicationKnowledge,
    )
    from pymedplum.fhir.medicationrequest import (
        MedicationRequest,
        MedicationRequestDispenseRequest,
        MedicationRequestDispenseRequestInitialFill,
        MedicationRequestSubstitution,
    )
    from pymedplum.fhir.medicationstatement import MedicationStatement
    from pymedplum.fhir.medicinalproduct import (
        MedicinalProduct,
        MedicinalProductManufacturingBusinessOperation,
        MedicinalProductName,
        MedicinalProductNameCountryLanguage,
        MedicinalProductNameNamePart,
        MedicinalProductSpecialDesignation,
    )
    from pymedplum.fhir.medicinalproductauthorization import (
        MedicinalProductAuthorization,
        MedicinalProductAuthorizationJurisdictionalAuthorization,
        MedicinalProductAuthorizationProcedure,
    )
    from pymedplum.fhir.medicinalproductcontraindication import (
        MedicinalProductContraindication,
        MedicinalProductContraindicationOtherTherapy,
    )
    from pymedplum.fhir.medicinalproductindication import (
        MedicinalProductIndication,
        MedicinalProductIndicationOtherTherapy,
    )
    from pymedplum.fhir.medicinalproductingredient import (
        MedicinalProductIngredient,
        MedicinalProductIngredientSpecifiedSubstance,
        MedicinalProductIngredientSpecifiedSubstanceStrength,
        MedicinalProductIngredientSpecifiedSubstanceStrengthReferenceStrength,
        MedicinalProductIngredientSubstance,
    )
    from pymedplum.fhir.medicinalproductinteraction import (
        MedicinalProductInteraction,
        MedicinalProductInteractionInteractant,
    )
    from pymedplum.fhir.medicinalproductmanufactured import MedicinalProductManufactured
    from pymedplum.fhir.medicinalproductpackaged import (
        MedicinalProductPackaged,
        MedicinalProductPackagedBatchIdentifier,
        MedicinalProductPackagedPackageItem,
    )
    from pymedplum.fhir.medicinalproductpharmaceutical import (
        MedicinalProductPharmaceutical,
        MedicinalProductPharmaceuticalCharacteristics,
        MedicinalProductPharmaceuticalRouteOfAdministration,
        MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpecies,
        MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpeciesWithdrawalPeriod,
    )
    from pymedplum.fhir.medicinalproductundesirableeffect import (
        MedicinalProductUndesirableEffect,
    )
    from pymedplum.fhir.messagedefinition import (
        MessageDefinition,
        MessageDefinitionAllowedResponse,
        MessageDefinitionFocus,
    )
    from pymedplum.fhir.messageheader import (
        MessageHeader,
        MessageHeaderDestination,
        MessageHeaderResponse,
        MessageHeaderSource,
    )
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.metadataresource import MetadataResource
    from pymedplum.fhir.molecularsequence import (
        MolecularSequence,
        MolecularSequenceQuality,
        MolecularSequenceQualityRoc,
        MolecularSequenceReferenceSeq,
        MolecularSequenceRepository,
        MolecularSequenceStructureVariant,
        MolecularSequenceStructureVariantInner,
        MolecularSequenceStructureVariantOuter,
        MolecularSequenceVariant,
    )
    from pymedplum.fhir.money import Money
    from pymedplum.fhir.moneyquantity import MoneyQuantity
    from pymedplum.fhir.namingsystem import NamingSystem, NamingSystemUniqueId
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.nutritionorder import (
        NutritionOrder,
        NutritionOrderEnteralFormula,
        NutritionOrderEnteralFormulaAdministration,
        NutritionOrderOralDiet,
        NutritionOrderOralDietNutrient,
        NutritionOrderOralDietTexture,
        NutritionOrderSupplement,
    )
    from pymedplum.fhir.observation import (
        Observation,
        ObservationComponent,
        ObservationReferenceRange,
    )
    from pymedplum.fhir.observationdefinition import (
        ObservationDefinition,
        ObservationDefinitionQualifiedInterval,
        ObservationDefinitionQuantitativeDetails,
    )
    from pymedplum.fhir.operationdefinition import (
        OperationDefinition,
        OperationDefinitionOverload,
        OperationDefinitionParameter,
        OperationDefinitionParameterBinding,
        OperationDefinitionParameterReferencedFrom,
    )
    from pymedplum.fhir.operationoutcome import OperationOutcome, OperationOutcomeIssue
    from pymedplum.fhir.organization import Organization, OrganizationContact
    from pymedplum.fhir.organizationaffiliation import OrganizationAffiliation
    from pymedplum.fhir.parameterdefinition import ParameterDefinition
    from pymedplum.fhir.parameters import Parameters, ParametersParameter
    from pymedplum.fhir.passwordchangerequest import PasswordChangeRequest
    from pymedplum.fhir.patient import (
        Patient,
        PatientCommunication,
        PatientContact,
        PatientLink,
    )
    from pymedplum.fhir.paymentnotice import PaymentNotice
    from pymedplum.fhir.paymentreconciliation import (
        PaymentReconciliation,
        PaymentReconciliationDetail,
        PaymentReconciliationProcessNote,
    )
    from pymedplum.fhir.period import Period
    from pymedplum.fhir.person import Person, PersonLink
    from pymedplum.fhir.plandefinition import (
        PlanDefinition,
        PlanDefinitionAction,
        PlanDefinitionActionCondition,
        PlanDefinitionActionDynamicValue,
        PlanDefinitionActionParticipant,
        PlanDefinitionActionRelatedAction,
        PlanDefinitionGoal,
        PlanDefinitionGoalTarget,
    )
    from pymedplum.fhir.population import Population
    from pymedplum.fhir.practitioner import Practitioner, PractitionerQualification
    from pymedplum.fhir.practitionerrole import (
        PractitionerRole,
        PractitionerRoleAvailableTime,
        PractitionerRoleNotAvailable,
    )
    from pymedplum.fhir.procedure import (
        Procedure,
        ProcedureFocalDevice,
        ProcedurePerformer,
    )
    from pymedplum.fhir.prodcharacteristic import ProdCharacteristic
    from pymedplum.fhir.productshelflife import ProductShelfLife
    from pymedplum.fhir.project import (
        Project,
        ProjectDefaultProfile,
        ProjectLink,
        ProjectSetting,
        ProjectSite,
    )
    from pymedplum.fhir.projectmembership import (
        ProjectMembership,
        ProjectMembershipAccess,
        ProjectMembershipAccessParameter,
    )
    from pymedplum.fhir.provenance import Provenance, ProvenanceAgent, ProvenanceEntity
    from pymedplum.fhir.quantity import Quantity
    from pymedplum.fhir.questionnaire import (
        Questionnaire,
        QuestionnaireItem,
        QuestionnaireItemAnswerOption,
        QuestionnaireItemEnableWhen,
        QuestionnaireItemInitial,
    )
    from pymedplum.fhir.questionnaireresponse import (
        QuestionnaireResponse,
        QuestionnaireResponseItem,
        QuestionnaireResponseItemAnswer,
    )
    from pymedplum.fhir.range import Range
    from pymedplum.fhir.ratio import Ratio
    from pymedplum.fhir.reference import Reference
    from pymedplum.fhir.relatedartifact import RelatedArtifact
    from pymedplum.fhir.relatedperson import RelatedPerson, RelatedPersonCommunication
    from pymedplum.fhir.requestgroup import (
        RequestGroup,
        RequestGroupAction,
        RequestGroupActionCondition,
        RequestGroupActionRelatedAction,
    )
    from pymedplum.fhir.researchdefinition import ResearchDefinition
    from pymedplum.fhir.researchelementdefinition import (
        ResearchElementDefinition,
        ResearchElementDefinitionCharacteristic,
    )
    from pymedplum.fhir.researchstudy import (
        ResearchStudy,
        ResearchStudyArm,
        ResearchStudyAssociatedParty,
        ResearchStudyComparisonGroup,
        ResearchStudyLabel,
        ResearchStudyObjective,
        ResearchStudyOutcomeMeasure,
        ResearchStudyProgressStatus,
        ResearchStudyRecruitment,
    )
    from pymedplum.fhir.researchsubject import ResearchSubject
    from pymedplum.fhir.riskassessment import RiskAssessment, RiskAssessmentPrediction
    from pymedplum.fhir.riskevidencesynthesis import (
        RiskEvidenceSynthesis,
        RiskEvidenceSynthesisCertainty,
        RiskEvidenceSynthesisCertaintyCertaintySubcomponent,
        RiskEvidenceSynthesisRiskEstimate,
        RiskEvidenceSynthesisRiskEstimatePrecisionEstimate,
        RiskEvidenceSynthesisSampleSize,
    )
    from pymedplum.fhir.sampleddata import SampledData
    from pymedplum.fhir.schedule import Schedule
    from pymedplum.fhir.searchparameter import SearchParameter, SearchParameterComponent
    from pymedplum.fhir.servicerequest import ServiceRequest
    from pymedplum.fhir.signature import Signature
    from pymedplum.fhir.simplequantity import SimpleQuantity
    from pymedplum.fhir.slot import Slot
    from pymedplum.fhir.smartapplaunch import SmartAppLaunch
    from pymedplum.fhir.specimen import (
        Specimen,
        SpecimenCollection,
        SpecimenContainer,
        SpecimenProcessing,
    )
    from pymedplum.fhir.specimendefinition import (
        SpecimenDefinition,
        SpecimenDefinitionTypeTested,
        SpecimenDefinitionTypeTestedContainer,
        SpecimenDefinitionTypeTestedContainerAdditive,
        SpecimenDefinitionTypeTestedHandling,
    )
    from pymedplum.fhir.structuredefinition import (
        StructureDefinition,
        StructureDefinitionContext,
        StructureDefinitionDifferential,
        StructureDefinitionMapping,
        StructureDefinitionSnapshot,
    )
    from pymedplum.fhir.structuremap import (
        StructureMap,
        StructureMapGroup,
        StructureMapGroupInput,
        StructureMapGroupRule,
        StructureMapGroupRuleDependent,
        StructureMapGroupRuleSource,
        StructureMapGroupRuleTarget,
        StructureMapGroupRuleTargetParameter,
        StructureMapStructure,
    )
    from pymedplum.fhir.subscription import Subscription, SubscriptionChannel
    from pymedplum.fhir.subscriptionstatus import (
        SubscriptionStatus,
        SubscriptionStatusNotificationEvent,
    )
    from pymedplum.fhir.substance import (
        Substance,
        SubstanceIngredient,
        SubstanceInstance,
    )
    from pymedplum.fhir.substanceamount import (
        SubstanceAmount,
        SubstanceAmountReferenceRange,
    )
    from pymedplum.fhir.substancenucleicacid import (
        SubstanceNucleicAcid,
        SubstanceNucleicAcidSubunit,
        SubstanceNucleicAcidSubunitLinkage,
        SubstanceNucleicAcidSubunitSugar,
    )
    from pymedplum.fhir.substancepolymer import (
        SubstancePolymer,
        SubstancePolymerMonomerSet,
        SubstancePolymerMonomerSetStartingMaterial,
        SubstancePolymerRepeat,
        SubstancePolymerRepeatRepeatUnit,
        SubstancePolymerRepeatRepeatUnitDegreeOfPolymerisation,
        SubstancePolymerRepeatRepeatUnitStructuralRepresentation,
    )
    from pymedplum.fhir.substanceprotein import (
        SubstanceProtein,
        SubstanceProteinSubunit,
    )
    from pymedplum.fhir.substancereferenceinformation import (
        SubstanceReferenceInformation,
        SubstanceReferenceInformationClassification,
        SubstanceReferenceInformationGene,
        SubstanceReferenceInformationGeneElement,
        SubstanceReferenceInformationTarget,
    )
    from pymedplum.fhir.substancesourcematerial import (
        SubstanceSourceMaterial,
        SubstanceSourceMaterialFractionDescription,
        SubstanceSourceMaterialOrganism,
        SubstanceSourceMaterialOrganismAuthor,
        SubstanceSourceMaterialOrganismHybrid,
        SubstanceSourceMaterialOrganismOrganismGeneral,
        SubstanceSourceMaterialPartDescription,
    )
    from pymedplum.fhir.substancespecification import (
        SubstanceSpecification,
        SubstanceSpecificationCode,
        SubstanceSpecificationMoiety,
        SubstanceSpecificationName,
        SubstanceSpecificationNameOfficial,
        SubstanceSpecificationProperty,
        SubstanceSpecificationRelationship,
        SubstanceSpecificationStructure,
        SubstanceSpecificationStructureIsotope,
        SubstanceSpecificationStructureIsotopeMolecularWeight,
        SubstanceSpecificationStructureRepresentation,
    )
    from pymedplum.fhir.supplydelivery import SupplyDelivery, SupplyDeliverySuppliedItem
    from pymedplum.fhir.supplyrequest import SupplyRequest, SupplyRequestParameter
    from pymedplum.fhir.task import Task, TaskInput, TaskOutput, TaskRestriction
    from pymedplum.fhir.terminologycapabilities import (
        TerminologyCapabilities,
        TerminologyCapabilitiesClosure,
        TerminologyCapabilitiesCodeSystem,
        TerminologyCapabilitiesCodeSystemVersion,
        TerminologyCapabilitiesCodeSystemVersionFilter,
        TerminologyCapabilitiesExpansion,
        TerminologyCapabilitiesExpansionParameter,
        TerminologyCapabilitiesImplementation,
        TerminologyCapabilitiesSoftware,
        TerminologyCapabilitiesTranslation,
        TerminologyCapabilitiesValidateCode,
    )
    from pymedplum.fhir.testreport import (
        TestReport,
        TestReportParticipant,
        TestReportSetup,
        TestReportSetupAction,
        TestReportSetupActionAssert,
        TestReportSetupActionOperation,
        TestReportTeardown,
        TestReportTeardownAction,
        TestReportTest,
        TestReportTestAction,
    )
    from pymedplum.fhir.testscript import (
        TestScript,
        TestScriptDestination,
        TestScriptFixture,
        TestScriptMetadata,
        TestScriptMetadataCapability,
        TestScriptMetadataLink,
        TestScriptOrigin,
        TestScriptSetup,
        TestScriptSetupAction,
        TestScriptSetupActionAssert,
        TestScriptSetupActionOperation,
        TestScriptSetupActionOperationRequestHeader,
        TestScriptTeardown,
        TestScriptTeardownAction,
        TestScriptTest,
        TestScriptTestAction,
        TestScriptVariable,
    )
    from pymedplum.fhir.timing import Timing, TimingRepeat
    from pymedplum.fhir.triggerdefinition import TriggerDefinition
    from pymedplum.fhir.usagecontext import UsageContext
    from pymedplum.fhir.user import User
    from pymedplum.fhir.userconfiguration import (
        UserConfiguration,
        UserConfigurationMenu,
        UserConfigurationMenuLink,
        UserConfigurationOption,
        UserConfigurationSearch,
    )
    from pymedplum.fhir.usersecurityrequest import UserSecurityRequest
    from pymedplum.fhir.valueset import (
        ValueSet,
        ValueSetCompose,
        ValueSetComposeInclude,
        ValueSetComposeIncludeConcept,
        ValueSetComposeIncludeConceptDesignation,
        ValueSetComposeIncludeFilter,
        ValueSetExpansion,
        ValueSetExpansionContains,
        ValueSetExpansionParameter,
    )
    from pymedplum.fhir.verificationresult import (
        VerificationResult,
        VerificationResultAttestation,
        VerificationResultPrimarySource,
        VerificationResultValidator,
    )
    from pymedplum.fhir.viewdefinition import (
        ViewDefinition,
        ViewDefinitionConstant,
        ViewDefinitionSelect,
        ViewDefinitionSelectColumn,
        ViewDefinitionSelectColumnTag,
        ViewDefinitionWhere,
    )
    from pymedplum.fhir.visionprescription import (
        VisionPrescription,
        VisionPrescriptionLensSpecification,
        VisionPrescriptionLensSpecificationPrism,
    )

    # Full type union for static analysis
    Resource = (
        AccessPolicy
        | AccessPolicyIpAccessRule
        | AccessPolicyResource
        | Account
        | AccountCoverage
        | AccountGuarantor
        | ActivityDefinition
        | ActivityDefinitionDynamicValue
        | ActivityDefinitionParticipant
        | Address
        | AdverseEvent
        | AdverseEventSuspectEntity
        | AdverseEventSuspectEntityCausality
        | Age
        | Agent
        | AgentChannel
        | AgentSetting
        | AllergyIntolerance
        | AllergyIntoleranceReaction
        | Annotation
        | Appointment
        | AppointmentParticipant
        | AppointmentResponse
        | AsyncJob
        | Attachment
        | AuditEvent
        | AuditEventAgent
        | AuditEventAgentNetwork
        | AuditEventEntity
        | AuditEventEntityDetail
        | AuditEventSource
        | BackboneElement
        | Basic
        | Binary
        | BiologicallyDerivedProduct
        | BiologicallyDerivedProductCollection
        | BiologicallyDerivedProductManipulation
        | BiologicallyDerivedProductProcessing
        | BiologicallyDerivedProductStorage
        | BodyStructure
        | Bot
        | BulkDataExport
        | BulkDataExportDeleted
        | BulkDataExportError
        | BulkDataExportOutput
        | Bundle
        | BundleEntry
        | BundleEntryRequest
        | BundleEntryResponse
        | BundleEntrySearch
        | BundleLink
        | CapabilityStatement
        | CapabilityStatementDocument
        | CapabilityStatementImplementation
        | CapabilityStatementMessaging
        | CapabilityStatementMessagingEndpoint
        | CapabilityStatementMessagingSupportedMessage
        | CapabilityStatementRest
        | CapabilityStatementRestInteraction
        | CapabilityStatementRestResource
        | CapabilityStatementRestResourceInteraction
        | CapabilityStatementRestResourceOperation
        | CapabilityStatementRestResourceSearchParam
        | CapabilityStatementRestSecurity
        | CapabilityStatementSoftware
        | CarePlan
        | CarePlanActivity
        | CarePlanActivityDetail
        | CareTeam
        | CareTeamParticipant
        | CatalogEntry
        | CatalogEntryRelatedEntry
        | ChargeItem
        | ChargeItemDefinition
        | ChargeItemDefinitionApplicability
        | ChargeItemDefinitionPropertyGroup
        | ChargeItemDefinitionPropertyGroupPriceComponent
        | ChargeItemPerformer
        | Claim
        | ClaimAccident
        | ClaimCareTeam
        | ClaimDiagnosis
        | ClaimInsurance
        | ClaimItem
        | ClaimItemDetail
        | ClaimItemDetailSubDetail
        | ClaimPayee
        | ClaimProcedure
        | ClaimRelated
        | ClaimResponse
        | ClaimResponseAddItem
        | ClaimResponseAddItemDetail
        | ClaimResponseAddItemDetailSubDetail
        | ClaimResponseError
        | ClaimResponseInsurance
        | ClaimResponseItem
        | ClaimResponseItemAdjudication
        | ClaimResponseItemDetail
        | ClaimResponseItemDetailSubDetail
        | ClaimResponsePayment
        | ClaimResponseProcessNote
        | ClaimResponseTotal
        | ClaimSupportingInfo
        | ClientApplication
        | ClientApplicationSignInForm
        | ClinicalImpression
        | ClinicalImpressionFinding
        | ClinicalImpressionInvestigation
        | CodeSystem
        | CodeSystemConcept
        | CodeSystemConceptDesignation
        | CodeSystemConceptProperty
        | CodeSystemFilter
        | CodeSystemProperty
        | CodeableConcept
        | Coding
        | Communication
        | CommunicationPayload
        | CommunicationRequest
        | CommunicationRequestPayload
        | CompartmentDefinition
        | CompartmentDefinitionResource
        | Composition
        | CompositionAttester
        | CompositionEvent
        | CompositionRelatesTo
        | CompositionSection
        | ConceptMap
        | ConceptMapGroup
        | ConceptMapGroupElement
        | ConceptMapGroupElementTarget
        | ConceptMapGroupElementTargetDependsOn
        | ConceptMapGroupUnmapped
        | Condition
        | ConditionEvidence
        | ConditionStage
        | Consent
        | ConsentPolicy
        | ConsentProvision
        | ConsentProvisionActor
        | ConsentProvisionData
        | ConsentVerification
        | ContactDetail
        | ContactPoint
        | Contract
        | ContractContentDefinition
        | ContractFriendly
        | ContractLegal
        | ContractRule
        | ContractSigner
        | ContractTerm
        | ContractTermAction
        | ContractTermActionSubject
        | ContractTermAsset
        | ContractTermAssetContext
        | ContractTermAssetValuedItem
        | ContractTermOffer
        | ContractTermOfferAnswer
        | ContractTermOfferParty
        | ContractTermSecurityLabel
        | Contributor
        | Count
        | Coverage
        | CoverageClass
        | CoverageCostToBeneficiary
        | CoverageCostToBeneficiaryException
        | CoverageEligibilityRequest
        | CoverageEligibilityRequestInsurance
        | CoverageEligibilityRequestItem
        | CoverageEligibilityRequestItemDiagnosis
        | CoverageEligibilityRequestSupportingInfo
        | CoverageEligibilityResponse
        | CoverageEligibilityResponseError
        | CoverageEligibilityResponseInsurance
        | CoverageEligibilityResponseInsuranceItem
        | CoverageEligibilityResponseInsuranceItemBenefit
        | DataRequirement
        | DataRequirementCodeFilter
        | DataRequirementDateFilter
        | DataRequirementSort
        | DetectedIssue
        | DetectedIssueEvidence
        | DetectedIssueMitigation
        | Device
        | DeviceDefinition
        | DeviceDefinitionCapability
        | DeviceDefinitionClassification
        | DeviceDefinitionDeviceName
        | DeviceDefinitionMaterial
        | DeviceDefinitionProperty
        | DeviceDefinitionSpecialization
        | DeviceDefinitionUdiDeviceIdentifier
        | DeviceDeviceName
        | DeviceMetric
        | DeviceMetricCalibration
        | DeviceProperty
        | DeviceRequest
        | DeviceRequestParameter
        | DeviceSpecialization
        | DeviceUdiCarrier
        | DeviceUseStatement
        | DeviceVersion
        | DiagnosticReport
        | DiagnosticReportMedia
        | Distance
        | DocumentManifest
        | DocumentManifestRelated
        | DocumentReference
        | DocumentReferenceContent
        | DocumentReferenceContext
        | DocumentReferenceRelatesTo
        | DomainConfiguration
        | Dosage
        | DosageDoseAndRate
        | Duration
        | EffectEvidenceSynthesis
        | EffectEvidenceSynthesisCertainty
        | EffectEvidenceSynthesisCertaintyCertaintySubcomponent
        | EffectEvidenceSynthesisEffectEstimate
        | EffectEvidenceSynthesisEffectEstimatePrecisionEstimate
        | EffectEvidenceSynthesisResultsByExposure
        | EffectEvidenceSynthesisSampleSize
        | Element
        | ElementDefinition
        | ElementDefinitionBase
        | ElementDefinitionBinding
        | ElementDefinitionConstraint
        | ElementDefinitionExample
        | ElementDefinitionMapping
        | ElementDefinitionSlicing
        | ElementDefinitionSlicingDiscriminator
        | ElementDefinitionType
        | Encounter
        | EncounterClassHistory
        | EncounterDiagnosis
        | EncounterHospitalization
        | EncounterLocation
        | EncounterParticipant
        | EncounterStatusHistory
        | Endpoint
        | EnrollmentRequest
        | EnrollmentResponse
        | EpisodeOfCare
        | EpisodeOfCareDiagnosis
        | EpisodeOfCareStatusHistory
        | EventDefinition
        | Evidence
        | EvidenceVariable
        | EvidenceVariableCharacteristic
        | EvidenceVariableCharacteristicDefinitionByCombination
        | EvidenceVariableCharacteristicDefinitionByTypeAndValue
        | EvidenceVariableCharacteristicTimeFromEvent
        | ExampleScenario
        | ExampleScenarioActor
        | ExampleScenarioInstance
        | ExampleScenarioInstanceContainedInstance
        | ExampleScenarioInstanceVersion
        | ExampleScenarioProcess
        | ExampleScenarioProcessStep
        | ExampleScenarioProcessStepAlternative
        | ExampleScenarioProcessStepOperation
        | ExplanationOfBenefit
        | ExplanationOfBenefitAccident
        | ExplanationOfBenefitAddItem
        | ExplanationOfBenefitAddItemDetail
        | ExplanationOfBenefitAddItemDetailSubDetail
        | ExplanationOfBenefitBenefitBalance
        | ExplanationOfBenefitBenefitBalanceFinancial
        | ExplanationOfBenefitCareTeam
        | ExplanationOfBenefitDiagnosis
        | ExplanationOfBenefitInsurance
        | ExplanationOfBenefitItem
        | ExplanationOfBenefitItemAdjudication
        | ExplanationOfBenefitItemDetail
        | ExplanationOfBenefitItemDetailSubDetail
        | ExplanationOfBenefitPayee
        | ExplanationOfBenefitPayment
        | ExplanationOfBenefitProcedure
        | ExplanationOfBenefitProcessNote
        | ExplanationOfBenefitRelated
        | ExplanationOfBenefitSupportingInfo
        | ExplanationOfBenefitTotal
        | Expression
        | Extension
        | FamilyMemberHistory
        | FamilyMemberHistoryCondition
        | Flag
        | Goal
        | GoalTarget
        | GraphDefinition
        | GraphDefinitionLink
        | GraphDefinitionLinkTarget
        | GraphDefinitionLinkTargetCompartment
        | Group
        | GroupCharacteristic
        | GroupMember
        | GuidanceResponse
        | HealthcareService
        | HealthcareServiceAvailableTime
        | HealthcareServiceEligibility
        | HealthcareServiceNotAvailable
        | HumanName
        | Identifier
        | IdentityProvider
        | ImagingStudy
        | ImagingStudySeries
        | ImagingStudySeriesInstance
        | ImagingStudySeriesPerformer
        | Immunization
        | ImmunizationEducation
        | ImmunizationEvaluation
        | ImmunizationPerformer
        | ImmunizationProtocolApplied
        | ImmunizationReaction
        | ImmunizationRecommendation
        | ImmunizationRecommendationRecommendation
        | ImmunizationRecommendationRecommendationDateCriterion
        | ImplementationGuide
        | ImplementationGuideDefinition
        | ImplementationGuideDefinitionGrouping
        | ImplementationGuideDefinitionPage
        | ImplementationGuideDefinitionParameter
        | ImplementationGuideDefinitionResource
        | ImplementationGuideDefinitionTemplate
        | ImplementationGuideDependsOn
        | ImplementationGuideGlobal
        | ImplementationGuideManifest
        | ImplementationGuideManifestPage
        | ImplementationGuideManifestResource
        | InsurancePlan
        | InsurancePlanContact
        | InsurancePlanCoverage
        | InsurancePlanCoverageBenefit
        | InsurancePlanCoverageBenefitLimit
        | InsurancePlanPlan
        | InsurancePlanPlanGeneralCost
        | InsurancePlanPlanSpecificCost
        | InsurancePlanPlanSpecificCostBenefit
        | InsurancePlanPlanSpecificCostBenefitCost
        | Invoice
        | InvoiceLineItem
        | InvoiceLineItemPriceComponent
        | InvoiceParticipant
        | JsonWebKey
        | Library
        | Linkage
        | LinkageItem
        | List
        | ListEntry
        | Location
        | LocationHoursOfOperation
        | LocationPosition
        | Login
        | MarketingStatus
        | Measure
        | MeasureGroup
        | MeasureGroupPopulation
        | MeasureGroupStratifier
        | MeasureGroupStratifierComponent
        | MeasureReport
        | MeasureReportGroup
        | MeasureReportGroupPopulation
        | MeasureReportGroupStratifier
        | MeasureReportGroupStratifierStratum
        | MeasureReportGroupStratifierStratumComponent
        | MeasureReportGroupStratifierStratumPopulation
        | MeasureSupplementalData
        | Media
        | Medication
        | MedicationAdministration
        | MedicationAdministrationDosage
        | MedicationAdministrationPerformer
        | MedicationBatch
        | MedicationDispense
        | MedicationDispensePerformer
        | MedicationDispenseSubstitution
        | MedicationIngredient
        | MedicationKnowledge
        | MedicationKnowledgeAdministrationGuidelines
        | MedicationKnowledgeAdministrationGuidelinesDosage
        | MedicationKnowledgeAdministrationGuidelinesPatientCharacteristics
        | MedicationKnowledgeCost
        | MedicationKnowledgeDrugCharacteristic
        | MedicationKnowledgeIngredient
        | MedicationKnowledgeKinetics
        | MedicationKnowledgeMedicineClassification
        | MedicationKnowledgeMonitoringProgram
        | MedicationKnowledgeMonograph
        | MedicationKnowledgePackaging
        | MedicationKnowledgeRegulatory
        | MedicationKnowledgeRegulatoryMaxDispense
        | MedicationKnowledgeRegulatorySchedule
        | MedicationKnowledgeRegulatorySubstitution
        | MedicationKnowledgeRelatedMedicationKnowledge
        | MedicationRequest
        | MedicationRequestDispenseRequest
        | MedicationRequestDispenseRequestInitialFill
        | MedicationRequestSubstitution
        | MedicationStatement
        | MedicinalProduct
        | MedicinalProductAuthorization
        | MedicinalProductAuthorizationJurisdictionalAuthorization
        | MedicinalProductAuthorizationProcedure
        | MedicinalProductContraindication
        | MedicinalProductContraindicationOtherTherapy
        | MedicinalProductIndication
        | MedicinalProductIndicationOtherTherapy
        | MedicinalProductIngredient
        | MedicinalProductIngredientSpecifiedSubstance
        | MedicinalProductIngredientSpecifiedSubstanceStrength
        | MedicinalProductIngredientSpecifiedSubstanceStrengthReferenceStrength
        | MedicinalProductIngredientSubstance
        | MedicinalProductInteraction
        | MedicinalProductInteractionInteractant
        | MedicinalProductManufactured
        | MedicinalProductManufacturingBusinessOperation
        | MedicinalProductName
        | MedicinalProductNameCountryLanguage
        | MedicinalProductNameNamePart
        | MedicinalProductPackaged
        | MedicinalProductPackagedBatchIdentifier
        | MedicinalProductPackagedPackageItem
        | MedicinalProductPharmaceutical
        | MedicinalProductPharmaceuticalCharacteristics
        | MedicinalProductPharmaceuticalRouteOfAdministration
        | MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpecies
        | MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpeciesWithdrawalPeriod
        | MedicinalProductSpecialDesignation
        | MedicinalProductUndesirableEffect
        | MessageDefinition
        | MessageDefinitionAllowedResponse
        | MessageDefinitionFocus
        | MessageHeader
        | MessageHeaderDestination
        | MessageHeaderResponse
        | MessageHeaderSource
        | Meta
        | MetadataResource
        | MolecularSequence
        | MolecularSequenceQuality
        | MolecularSequenceQualityRoc
        | MolecularSequenceReferenceSeq
        | MolecularSequenceRepository
        | MolecularSequenceStructureVariant
        | MolecularSequenceStructureVariantInner
        | MolecularSequenceStructureVariantOuter
        | MolecularSequenceVariant
        | Money
        | MoneyQuantity
        | NamingSystem
        | NamingSystemUniqueId
        | Narrative
        | NutritionOrder
        | NutritionOrderEnteralFormula
        | NutritionOrderEnteralFormulaAdministration
        | NutritionOrderOralDiet
        | NutritionOrderOralDietNutrient
        | NutritionOrderOralDietTexture
        | NutritionOrderSupplement
        | Observation
        | ObservationComponent
        | ObservationDefinition
        | ObservationDefinitionQualifiedInterval
        | ObservationDefinitionQuantitativeDetails
        | ObservationReferenceRange
        | OperationDefinition
        | OperationDefinitionOverload
        | OperationDefinitionParameter
        | OperationDefinitionParameterBinding
        | OperationDefinitionParameterReferencedFrom
        | OperationOutcome
        | OperationOutcomeIssue
        | Organization
        | OrganizationAffiliation
        | OrganizationContact
        | ParameterDefinition
        | Parameters
        | ParametersParameter
        | PasswordChangeRequest
        | Patient
        | PatientCommunication
        | PatientContact
        | PatientLink
        | PaymentNotice
        | PaymentReconciliation
        | PaymentReconciliationDetail
        | PaymentReconciliationProcessNote
        | Period
        | Person
        | PersonLink
        | PlanDefinition
        | PlanDefinitionAction
        | PlanDefinitionActionCondition
        | PlanDefinitionActionDynamicValue
        | PlanDefinitionActionParticipant
        | PlanDefinitionActionRelatedAction
        | PlanDefinitionGoal
        | PlanDefinitionGoalTarget
        | Population
        | Practitioner
        | PractitionerQualification
        | PractitionerRole
        | PractitionerRoleAvailableTime
        | PractitionerRoleNotAvailable
        | Procedure
        | ProcedureFocalDevice
        | ProcedurePerformer
        | ProdCharacteristic
        | ProductShelfLife
        | Project
        | ProjectDefaultProfile
        | ProjectLink
        | ProjectMembership
        | ProjectMembershipAccess
        | ProjectMembershipAccessParameter
        | ProjectSetting
        | ProjectSite
        | Provenance
        | ProvenanceAgent
        | ProvenanceEntity
        | Quantity
        | Questionnaire
        | QuestionnaireItem
        | QuestionnaireItemAnswerOption
        | QuestionnaireItemEnableWhen
        | QuestionnaireItemInitial
        | QuestionnaireResponse
        | QuestionnaireResponseItem
        | QuestionnaireResponseItemAnswer
        | Range
        | Ratio
        | Reference
        | RelatedArtifact
        | RelatedPerson
        | RelatedPersonCommunication
        | RequestGroup
        | RequestGroupAction
        | RequestGroupActionCondition
        | RequestGroupActionRelatedAction
        | ResearchDefinition
        | ResearchElementDefinition
        | ResearchElementDefinitionCharacteristic
        | ResearchStudy
        | ResearchStudyArm
        | ResearchStudyAssociatedParty
        | ResearchStudyComparisonGroup
        | ResearchStudyLabel
        | ResearchStudyObjective
        | ResearchStudyOutcomeMeasure
        | ResearchStudyProgressStatus
        | ResearchStudyRecruitment
        | ResearchSubject
        | RiskAssessment
        | RiskAssessmentPrediction
        | RiskEvidenceSynthesis
        | RiskEvidenceSynthesisCertainty
        | RiskEvidenceSynthesisCertaintyCertaintySubcomponent
        | RiskEvidenceSynthesisRiskEstimate
        | RiskEvidenceSynthesisRiskEstimatePrecisionEstimate
        | RiskEvidenceSynthesisSampleSize
        | SampledData
        | Schedule
        | SearchParameter
        | SearchParameterComponent
        | ServiceRequest
        | Signature
        | SimpleQuantity
        | Slot
        | SmartAppLaunch
        | Specimen
        | SpecimenCollection
        | SpecimenContainer
        | SpecimenDefinition
        | SpecimenDefinitionTypeTested
        | SpecimenDefinitionTypeTestedContainer
        | SpecimenDefinitionTypeTestedContainerAdditive
        | SpecimenDefinitionTypeTestedHandling
        | SpecimenProcessing
        | StructureDefinition
        | StructureDefinitionContext
        | StructureDefinitionDifferential
        | StructureDefinitionMapping
        | StructureDefinitionSnapshot
        | StructureMap
        | StructureMapGroup
        | StructureMapGroupInput
        | StructureMapGroupRule
        | StructureMapGroupRuleDependent
        | StructureMapGroupRuleSource
        | StructureMapGroupRuleTarget
        | StructureMapGroupRuleTargetParameter
        | StructureMapStructure
        | Subscription
        | SubscriptionChannel
        | SubscriptionStatus
        | SubscriptionStatusNotificationEvent
        | Substance
        | SubstanceAmount
        | SubstanceAmountReferenceRange
        | SubstanceIngredient
        | SubstanceInstance
        | SubstanceNucleicAcid
        | SubstanceNucleicAcidSubunit
        | SubstanceNucleicAcidSubunitLinkage
        | SubstanceNucleicAcidSubunitSugar
        | SubstancePolymer
        | SubstancePolymerMonomerSet
        | SubstancePolymerMonomerSetStartingMaterial
        | SubstancePolymerRepeat
        | SubstancePolymerRepeatRepeatUnit
        | SubstancePolymerRepeatRepeatUnitDegreeOfPolymerisation
        | SubstancePolymerRepeatRepeatUnitStructuralRepresentation
        | SubstanceProtein
        | SubstanceProteinSubunit
        | SubstanceReferenceInformation
        | SubstanceReferenceInformationClassification
        | SubstanceReferenceInformationGene
        | SubstanceReferenceInformationGeneElement
        | SubstanceReferenceInformationTarget
        | SubstanceSourceMaterial
        | SubstanceSourceMaterialFractionDescription
        | SubstanceSourceMaterialOrganism
        | SubstanceSourceMaterialOrganismAuthor
        | SubstanceSourceMaterialOrganismHybrid
        | SubstanceSourceMaterialOrganismOrganismGeneral
        | SubstanceSourceMaterialPartDescription
        | SubstanceSpecification
        | SubstanceSpecificationCode
        | SubstanceSpecificationMoiety
        | SubstanceSpecificationName
        | SubstanceSpecificationNameOfficial
        | SubstanceSpecificationProperty
        | SubstanceSpecificationRelationship
        | SubstanceSpecificationStructure
        | SubstanceSpecificationStructureIsotope
        | SubstanceSpecificationStructureIsotopeMolecularWeight
        | SubstanceSpecificationStructureRepresentation
        | SupplyDelivery
        | SupplyDeliverySuppliedItem
        | SupplyRequest
        | SupplyRequestParameter
        | Task
        | TaskInput
        | TaskOutput
        | TaskRestriction
        | TerminologyCapabilities
        | TerminologyCapabilitiesClosure
        | TerminologyCapabilitiesCodeSystem
        | TerminologyCapabilitiesCodeSystemVersion
        | TerminologyCapabilitiesCodeSystemVersionFilter
        | TerminologyCapabilitiesExpansion
        | TerminologyCapabilitiesExpansionParameter
        | TerminologyCapabilitiesImplementation
        | TerminologyCapabilitiesSoftware
        | TerminologyCapabilitiesTranslation
        | TerminologyCapabilitiesValidateCode
        | TestReport
        | TestReportParticipant
        | TestReportSetup
        | TestReportSetupAction
        | TestReportSetupActionAssert
        | TestReportSetupActionOperation
        | TestReportTeardown
        | TestReportTeardownAction
        | TestReportTest
        | TestReportTestAction
        | TestScript
        | TestScriptDestination
        | TestScriptFixture
        | TestScriptMetadata
        | TestScriptMetadataCapability
        | TestScriptMetadataLink
        | TestScriptOrigin
        | TestScriptSetup
        | TestScriptSetupAction
        | TestScriptSetupActionAssert
        | TestScriptSetupActionOperation
        | TestScriptSetupActionOperationRequestHeader
        | TestScriptTeardown
        | TestScriptTeardownAction
        | TestScriptTest
        | TestScriptTestAction
        | TestScriptVariable
        | Timing
        | TimingRepeat
        | TriggerDefinition
        | UsageContext
        | User
        | UserConfiguration
        | UserConfigurationMenu
        | UserConfigurationMenuLink
        | UserConfigurationOption
        | UserConfigurationSearch
        | UserSecurityRequest
        | ValueSet
        | ValueSetCompose
        | ValueSetComposeInclude
        | ValueSetComposeIncludeConcept
        | ValueSetComposeIncludeConceptDesignation
        | ValueSetComposeIncludeFilter
        | ValueSetExpansion
        | ValueSetExpansionContains
        | ValueSetExpansionParameter
        | VerificationResult
        | VerificationResultAttestation
        | VerificationResultPrimarySource
        | VerificationResultValidator
        | ViewDefinition
        | ViewDefinitionConstant
        | ViewDefinitionSelect
        | ViewDefinitionSelectColumn
        | ViewDefinitionSelectColumnTag
        | ViewDefinitionWhere
        | VisionPrescription
        | VisionPrescriptionLensSpecification
        | VisionPrescriptionLensSpecificationPrism
    )


# ============================================================================
# Module Exports
# ============================================================================

if TYPE_CHECKING:
    # For type checkers: export all resource names
    __all__ = [
        "AccessPolicy",
        "AccessPolicyIpAccessRule",
        "AccessPolicyResource",
        "Account",
        "AccountCoverage",
        "AccountGuarantor",
        "ActivityDefinition",
        "ActivityDefinitionDynamicValue",
        "ActivityDefinitionParticipant",
        "Address",
        "AdverseEvent",
        "AdverseEventSuspectEntity",
        "AdverseEventSuspectEntityCausality",
        "Age",
        "Agent",
        "AgentChannel",
        "AgentSetting",
        "AllergyIntolerance",
        "AllergyIntoleranceReaction",
        "Annotation",
        "Appointment",
        "AppointmentParticipant",
        "AppointmentResponse",
        "AsyncJob",
        "Attachment",
        "AuditEvent",
        "AuditEventAgent",
        "AuditEventAgentNetwork",
        "AuditEventEntity",
        "AuditEventEntityDetail",
        "AuditEventSource",
        "BackboneElement",
        "Basic",
        "Binary",
        "BiologicallyDerivedProduct",
        "BiologicallyDerivedProductCollection",
        "BiologicallyDerivedProductManipulation",
        "BiologicallyDerivedProductProcessing",
        "BiologicallyDerivedProductStorage",
        "BodyStructure",
        "Bot",
        "BulkDataExport",
        "BulkDataExportDeleted",
        "BulkDataExportError",
        "BulkDataExportOutput",
        "Bundle",
        "BundleEntry",
        "BundleEntryRequest",
        "BundleEntryResponse",
        "BundleEntrySearch",
        "BundleLink",
        "CapabilityStatement",
        "CapabilityStatementDocument",
        "CapabilityStatementImplementation",
        "CapabilityStatementMessaging",
        "CapabilityStatementMessagingEndpoint",
        "CapabilityStatementMessagingSupportedMessage",
        "CapabilityStatementRest",
        "CapabilityStatementRestInteraction",
        "CapabilityStatementRestResource",
        "CapabilityStatementRestResourceInteraction",
        "CapabilityStatementRestResourceOperation",
        "CapabilityStatementRestResourceSearchParam",
        "CapabilityStatementRestSecurity",
        "CapabilityStatementSoftware",
        "CarePlan",
        "CarePlanActivity",
        "CarePlanActivityDetail",
        "CareTeam",
        "CareTeamParticipant",
        "CatalogEntry",
        "CatalogEntryRelatedEntry",
        "ChargeItem",
        "ChargeItemDefinition",
        "ChargeItemDefinitionApplicability",
        "ChargeItemDefinitionPropertyGroup",
        "ChargeItemDefinitionPropertyGroupPriceComponent",
        "ChargeItemPerformer",
        "Claim",
        "ClaimAccident",
        "ClaimCareTeam",
        "ClaimDiagnosis",
        "ClaimInsurance",
        "ClaimItem",
        "ClaimItemDetail",
        "ClaimItemDetailSubDetail",
        "ClaimPayee",
        "ClaimProcedure",
        "ClaimRelated",
        "ClaimResponse",
        "ClaimResponseAddItem",
        "ClaimResponseAddItemDetail",
        "ClaimResponseAddItemDetailSubDetail",
        "ClaimResponseError",
        "ClaimResponseInsurance",
        "ClaimResponseItem",
        "ClaimResponseItemAdjudication",
        "ClaimResponseItemDetail",
        "ClaimResponseItemDetailSubDetail",
        "ClaimResponsePayment",
        "ClaimResponseProcessNote",
        "ClaimResponseTotal",
        "ClaimSupportingInfo",
        "ClientApplication",
        "ClientApplicationSignInForm",
        "ClinicalImpression",
        "ClinicalImpressionFinding",
        "ClinicalImpressionInvestigation",
        "CodeSystem",
        "CodeSystemConcept",
        "CodeSystemConceptDesignation",
        "CodeSystemConceptProperty",
        "CodeSystemFilter",
        "CodeSystemProperty",
        "CodeableConcept",
        "Coding",
        "Communication",
        "CommunicationPayload",
        "CommunicationRequest",
        "CommunicationRequestPayload",
        "CompartmentDefinition",
        "CompartmentDefinitionResource",
        "Composition",
        "CompositionAttester",
        "CompositionEvent",
        "CompositionRelatesTo",
        "CompositionSection",
        "ConceptMap",
        "ConceptMapGroup",
        "ConceptMapGroupElement",
        "ConceptMapGroupElementTarget",
        "ConceptMapGroupElementTargetDependsOn",
        "ConceptMapGroupUnmapped",
        "Condition",
        "ConditionEvidence",
        "ConditionStage",
        "Consent",
        "ConsentPolicy",
        "ConsentProvision",
        "ConsentProvisionActor",
        "ConsentProvisionData",
        "ConsentVerification",
        "ContactDetail",
        "ContactPoint",
        "Contract",
        "ContractContentDefinition",
        "ContractFriendly",
        "ContractLegal",
        "ContractRule",
        "ContractSigner",
        "ContractTerm",
        "ContractTermAction",
        "ContractTermActionSubject",
        "ContractTermAsset",
        "ContractTermAssetContext",
        "ContractTermAssetValuedItem",
        "ContractTermOffer",
        "ContractTermOfferAnswer",
        "ContractTermOfferParty",
        "ContractTermSecurityLabel",
        "Contributor",
        "Count",
        "Coverage",
        "CoverageClass",
        "CoverageCostToBeneficiary",
        "CoverageCostToBeneficiaryException",
        "CoverageEligibilityRequest",
        "CoverageEligibilityRequestInsurance",
        "CoverageEligibilityRequestItem",
        "CoverageEligibilityRequestItemDiagnosis",
        "CoverageEligibilityRequestSupportingInfo",
        "CoverageEligibilityResponse",
        "CoverageEligibilityResponseError",
        "CoverageEligibilityResponseInsurance",
        "CoverageEligibilityResponseInsuranceItem",
        "CoverageEligibilityResponseInsuranceItemBenefit",
        "DataRequirement",
        "DataRequirementCodeFilter",
        "DataRequirementDateFilter",
        "DataRequirementSort",
        "DetectedIssue",
        "DetectedIssueEvidence",
        "DetectedIssueMitigation",
        "Device",
        "DeviceDefinition",
        "DeviceDefinitionCapability",
        "DeviceDefinitionClassification",
        "DeviceDefinitionDeviceName",
        "DeviceDefinitionMaterial",
        "DeviceDefinitionProperty",
        "DeviceDefinitionSpecialization",
        "DeviceDefinitionUdiDeviceIdentifier",
        "DeviceDeviceName",
        "DeviceMetric",
        "DeviceMetricCalibration",
        "DeviceProperty",
        "DeviceRequest",
        "DeviceRequestParameter",
        "DeviceSpecialization",
        "DeviceUdiCarrier",
        "DeviceUseStatement",
        "DeviceVersion",
        "DiagnosticReport",
        "DiagnosticReportMedia",
        "Distance",
        "DocumentManifest",
        "DocumentManifestRelated",
        "DocumentReference",
        "DocumentReferenceContent",
        "DocumentReferenceContext",
        "DocumentReferenceRelatesTo",
        "DomainConfiguration",
        "Dosage",
        "DosageDoseAndRate",
        "Duration",
        "EffectEvidenceSynthesis",
        "EffectEvidenceSynthesisCertainty",
        "EffectEvidenceSynthesisCertaintyCertaintySubcomponent",
        "EffectEvidenceSynthesisEffectEstimate",
        "EffectEvidenceSynthesisEffectEstimatePrecisionEstimate",
        "EffectEvidenceSynthesisResultsByExposure",
        "EffectEvidenceSynthesisSampleSize",
        "Element",
        "ElementDefinition",
        "ElementDefinitionBase",
        "ElementDefinitionBinding",
        "ElementDefinitionConstraint",
        "ElementDefinitionExample",
        "ElementDefinitionMapping",
        "ElementDefinitionSlicing",
        "ElementDefinitionSlicingDiscriminator",
        "ElementDefinitionType",
        "Encounter",
        "EncounterClassHistory",
        "EncounterDiagnosis",
        "EncounterHospitalization",
        "EncounterLocation",
        "EncounterParticipant",
        "EncounterStatusHistory",
        "Endpoint",
        "EnrollmentRequest",
        "EnrollmentResponse",
        "EpisodeOfCare",
        "EpisodeOfCareDiagnosis",
        "EpisodeOfCareStatusHistory",
        "EventDefinition",
        "Evidence",
        "EvidenceVariable",
        "EvidenceVariableCharacteristic",
        "EvidenceVariableCharacteristicDefinitionByCombination",
        "EvidenceVariableCharacteristicDefinitionByTypeAndValue",
        "EvidenceVariableCharacteristicTimeFromEvent",
        "ExampleScenario",
        "ExampleScenarioActor",
        "ExampleScenarioInstance",
        "ExampleScenarioInstanceContainedInstance",
        "ExampleScenarioInstanceVersion",
        "ExampleScenarioProcess",
        "ExampleScenarioProcessStep",
        "ExampleScenarioProcessStepAlternative",
        "ExampleScenarioProcessStepOperation",
        "ExplanationOfBenefit",
        "ExplanationOfBenefitAccident",
        "ExplanationOfBenefitAddItem",
        "ExplanationOfBenefitAddItemDetail",
        "ExplanationOfBenefitAddItemDetailSubDetail",
        "ExplanationOfBenefitBenefitBalance",
        "ExplanationOfBenefitBenefitBalanceFinancial",
        "ExplanationOfBenefitCareTeam",
        "ExplanationOfBenefitDiagnosis",
        "ExplanationOfBenefitInsurance",
        "ExplanationOfBenefitItem",
        "ExplanationOfBenefitItemAdjudication",
        "ExplanationOfBenefitItemDetail",
        "ExplanationOfBenefitItemDetailSubDetail",
        "ExplanationOfBenefitPayee",
        "ExplanationOfBenefitPayment",
        "ExplanationOfBenefitProcedure",
        "ExplanationOfBenefitProcessNote",
        "ExplanationOfBenefitRelated",
        "ExplanationOfBenefitSupportingInfo",
        "ExplanationOfBenefitTotal",
        "Expression",
        "Extension",
        "FamilyMemberHistory",
        "FamilyMemberHistoryCondition",
        "Flag",
        "Goal",
        "GoalTarget",
        "GraphDefinition",
        "GraphDefinitionLink",
        "GraphDefinitionLinkTarget",
        "GraphDefinitionLinkTargetCompartment",
        "Group",
        "GroupCharacteristic",
        "GroupMember",
        "GuidanceResponse",
        "HealthcareService",
        "HealthcareServiceAvailableTime",
        "HealthcareServiceEligibility",
        "HealthcareServiceNotAvailable",
        "HumanName",
        "Identifier",
        "IdentityProvider",
        "ImagingStudy",
        "ImagingStudySeries",
        "ImagingStudySeriesInstance",
        "ImagingStudySeriesPerformer",
        "Immunization",
        "ImmunizationEducation",
        "ImmunizationEvaluation",
        "ImmunizationPerformer",
        "ImmunizationProtocolApplied",
        "ImmunizationReaction",
        "ImmunizationRecommendation",
        "ImmunizationRecommendationRecommendation",
        "ImmunizationRecommendationRecommendationDateCriterion",
        "ImplementationGuide",
        "ImplementationGuideDefinition",
        "ImplementationGuideDefinitionGrouping",
        "ImplementationGuideDefinitionPage",
        "ImplementationGuideDefinitionParameter",
        "ImplementationGuideDefinitionResource",
        "ImplementationGuideDefinitionTemplate",
        "ImplementationGuideDependsOn",
        "ImplementationGuideGlobal",
        "ImplementationGuideManifest",
        "ImplementationGuideManifestPage",
        "ImplementationGuideManifestResource",
        "InsurancePlan",
        "InsurancePlanContact",
        "InsurancePlanCoverage",
        "InsurancePlanCoverageBenefit",
        "InsurancePlanCoverageBenefitLimit",
        "InsurancePlanPlan",
        "InsurancePlanPlanGeneralCost",
        "InsurancePlanPlanSpecificCost",
        "InsurancePlanPlanSpecificCostBenefit",
        "InsurancePlanPlanSpecificCostBenefitCost",
        "Invoice",
        "InvoiceLineItem",
        "InvoiceLineItemPriceComponent",
        "InvoiceParticipant",
        "JsonWebKey",
        "Library",
        "Linkage",
        "LinkageItem",
        "List",
        "ListEntry",
        "Location",
        "LocationHoursOfOperation",
        "LocationPosition",
        "Login",
        "MarketingStatus",
        "Measure",
        "MeasureGroup",
        "MeasureGroupPopulation",
        "MeasureGroupStratifier",
        "MeasureGroupStratifierComponent",
        "MeasureReport",
        "MeasureReportGroup",
        "MeasureReportGroupPopulation",
        "MeasureReportGroupStratifier",
        "MeasureReportGroupStratifierStratum",
        "MeasureReportGroupStratifierStratumComponent",
        "MeasureReportGroupStratifierStratumPopulation",
        "MeasureSupplementalData",
        "Media",
        "Medication",
        "MedicationAdministration",
        "MedicationAdministrationDosage",
        "MedicationAdministrationPerformer",
        "MedicationBatch",
        "MedicationDispense",
        "MedicationDispensePerformer",
        "MedicationDispenseSubstitution",
        "MedicationIngredient",
        "MedicationKnowledge",
        "MedicationKnowledgeAdministrationGuidelines",
        "MedicationKnowledgeAdministrationGuidelinesDosage",
        "MedicationKnowledgeAdministrationGuidelinesPatientCharacteristics",
        "MedicationKnowledgeCost",
        "MedicationKnowledgeDrugCharacteristic",
        "MedicationKnowledgeIngredient",
        "MedicationKnowledgeKinetics",
        "MedicationKnowledgeMedicineClassification",
        "MedicationKnowledgeMonitoringProgram",
        "MedicationKnowledgeMonograph",
        "MedicationKnowledgePackaging",
        "MedicationKnowledgeRegulatory",
        "MedicationKnowledgeRegulatoryMaxDispense",
        "MedicationKnowledgeRegulatorySchedule",
        "MedicationKnowledgeRegulatorySubstitution",
        "MedicationKnowledgeRelatedMedicationKnowledge",
        "MedicationRequest",
        "MedicationRequestDispenseRequest",
        "MedicationRequestDispenseRequestInitialFill",
        "MedicationRequestSubstitution",
        "MedicationStatement",
        "MedicinalProduct",
        "MedicinalProductAuthorization",
        "MedicinalProductAuthorizationJurisdictionalAuthorization",
        "MedicinalProductAuthorizationProcedure",
        "MedicinalProductContraindication",
        "MedicinalProductContraindicationOtherTherapy",
        "MedicinalProductIndication",
        "MedicinalProductIndicationOtherTherapy",
        "MedicinalProductIngredient",
        "MedicinalProductIngredientSpecifiedSubstance",
        "MedicinalProductIngredientSpecifiedSubstanceStrength",
        "MedicinalProductIngredientSpecifiedSubstanceStrengthReferenceStrength",
        "MedicinalProductIngredientSubstance",
        "MedicinalProductInteraction",
        "MedicinalProductInteractionInteractant",
        "MedicinalProductManufactured",
        "MedicinalProductManufacturingBusinessOperation",
        "MedicinalProductName",
        "MedicinalProductNameCountryLanguage",
        "MedicinalProductNameNamePart",
        "MedicinalProductPackaged",
        "MedicinalProductPackagedBatchIdentifier",
        "MedicinalProductPackagedPackageItem",
        "MedicinalProductPharmaceutical",
        "MedicinalProductPharmaceuticalCharacteristics",
        "MedicinalProductPharmaceuticalRouteOfAdministration",
        "MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpecies",
        "MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpeciesWithdrawalPeriod",
        "MedicinalProductSpecialDesignation",
        "MedicinalProductUndesirableEffect",
        "MessageDefinition",
        "MessageDefinitionAllowedResponse",
        "MessageDefinitionFocus",
        "MessageHeader",
        "MessageHeaderDestination",
        "MessageHeaderResponse",
        "MessageHeaderSource",
        "Meta",
        "MetadataResource",
        "MolecularSequence",
        "MolecularSequenceQuality",
        "MolecularSequenceQualityRoc",
        "MolecularSequenceReferenceSeq",
        "MolecularSequenceRepository",
        "MolecularSequenceStructureVariant",
        "MolecularSequenceStructureVariantInner",
        "MolecularSequenceStructureVariantOuter",
        "MolecularSequenceVariant",
        "Money",
        "MoneyQuantity",
        "NamingSystem",
        "NamingSystemUniqueId",
        "Narrative",
        "NutritionOrder",
        "NutritionOrderEnteralFormula",
        "NutritionOrderEnteralFormulaAdministration",
        "NutritionOrderOralDiet",
        "NutritionOrderOralDietNutrient",
        "NutritionOrderOralDietTexture",
        "NutritionOrderSupplement",
        "Observation",
        "ObservationComponent",
        "ObservationDefinition",
        "ObservationDefinitionQualifiedInterval",
        "ObservationDefinitionQuantitativeDetails",
        "ObservationReferenceRange",
        "OperationDefinition",
        "OperationDefinitionOverload",
        "OperationDefinitionParameter",
        "OperationDefinitionParameterBinding",
        "OperationDefinitionParameterReferencedFrom",
        "OperationOutcome",
        "OperationOutcomeIssue",
        "Organization",
        "OrganizationAffiliation",
        "OrganizationContact",
        "ParameterDefinition",
        "Parameters",
        "ParametersParameter",
        "PasswordChangeRequest",
        "Patient",
        "PatientCommunication",
        "PatientContact",
        "PatientLink",
        "PaymentNotice",
        "PaymentReconciliation",
        "PaymentReconciliationDetail",
        "PaymentReconciliationProcessNote",
        "Period",
        "Person",
        "PersonLink",
        "PlanDefinition",
        "PlanDefinitionAction",
        "PlanDefinitionActionCondition",
        "PlanDefinitionActionDynamicValue",
        "PlanDefinitionActionParticipant",
        "PlanDefinitionActionRelatedAction",
        "PlanDefinitionGoal",
        "PlanDefinitionGoalTarget",
        "Population",
        "Practitioner",
        "PractitionerQualification",
        "PractitionerRole",
        "PractitionerRoleAvailableTime",
        "PractitionerRoleNotAvailable",
        "Procedure",
        "ProcedureFocalDevice",
        "ProcedurePerformer",
        "ProdCharacteristic",
        "ProductShelfLife",
        "Project",
        "ProjectDefaultProfile",
        "ProjectLink",
        "ProjectMembership",
        "ProjectMembershipAccess",
        "ProjectMembershipAccessParameter",
        "ProjectSetting",
        "ProjectSite",
        "Provenance",
        "ProvenanceAgent",
        "ProvenanceEntity",
        "Quantity",
        "Questionnaire",
        "QuestionnaireItem",
        "QuestionnaireItemAnswerOption",
        "QuestionnaireItemEnableWhen",
        "QuestionnaireItemInitial",
        "QuestionnaireResponse",
        "QuestionnaireResponseItem",
        "QuestionnaireResponseItemAnswer",
        "Range",
        "Ratio",
        "Reference",
        "RelatedArtifact",
        "RelatedPerson",
        "RelatedPersonCommunication",
        "RequestGroup",
        "RequestGroupAction",
        "RequestGroupActionCondition",
        "RequestGroupActionRelatedAction",
        "ResearchDefinition",
        "ResearchElementDefinition",
        "ResearchElementDefinitionCharacteristic",
        "ResearchStudy",
        "ResearchStudyArm",
        "ResearchStudyAssociatedParty",
        "ResearchStudyComparisonGroup",
        "ResearchStudyLabel",
        "ResearchStudyObjective",
        "ResearchStudyOutcomeMeasure",
        "ResearchStudyProgressStatus",
        "ResearchStudyRecruitment",
        "ResearchSubject",
        "Resource",
        "RiskAssessment",
        "RiskAssessmentPrediction",
        "RiskEvidenceSynthesis",
        "RiskEvidenceSynthesisCertainty",
        "RiskEvidenceSynthesisCertaintyCertaintySubcomponent",
        "RiskEvidenceSynthesisRiskEstimate",
        "RiskEvidenceSynthesisRiskEstimatePrecisionEstimate",
        "RiskEvidenceSynthesisSampleSize",
        "SampledData",
        "Schedule",
        "SearchParameter",
        "SearchParameterComponent",
        "ServiceRequest",
        "Signature",
        "SimpleQuantity",
        "Slot",
        "SmartAppLaunch",
        "Specimen",
        "SpecimenCollection",
        "SpecimenContainer",
        "SpecimenDefinition",
        "SpecimenDefinitionTypeTested",
        "SpecimenDefinitionTypeTestedContainer",
        "SpecimenDefinitionTypeTestedContainerAdditive",
        "SpecimenDefinitionTypeTestedHandling",
        "SpecimenProcessing",
        "StructureDefinition",
        "StructureDefinitionContext",
        "StructureDefinitionDifferential",
        "StructureDefinitionMapping",
        "StructureDefinitionSnapshot",
        "StructureMap",
        "StructureMapGroup",
        "StructureMapGroupInput",
        "StructureMapGroupRule",
        "StructureMapGroupRuleDependent",
        "StructureMapGroupRuleSource",
        "StructureMapGroupRuleTarget",
        "StructureMapGroupRuleTargetParameter",
        "StructureMapStructure",
        "Subscription",
        "SubscriptionChannel",
        "SubscriptionStatus",
        "SubscriptionStatusNotificationEvent",
        "Substance",
        "SubstanceAmount",
        "SubstanceAmountReferenceRange",
        "SubstanceIngredient",
        "SubstanceInstance",
        "SubstanceNucleicAcid",
        "SubstanceNucleicAcidSubunit",
        "SubstanceNucleicAcidSubunitLinkage",
        "SubstanceNucleicAcidSubunitSugar",
        "SubstancePolymer",
        "SubstancePolymerMonomerSet",
        "SubstancePolymerMonomerSetStartingMaterial",
        "SubstancePolymerRepeat",
        "SubstancePolymerRepeatRepeatUnit",
        "SubstancePolymerRepeatRepeatUnitDegreeOfPolymerisation",
        "SubstancePolymerRepeatRepeatUnitStructuralRepresentation",
        "SubstanceProtein",
        "SubstanceProteinSubunit",
        "SubstanceReferenceInformation",
        "SubstanceReferenceInformationClassification",
        "SubstanceReferenceInformationGene",
        "SubstanceReferenceInformationGeneElement",
        "SubstanceReferenceInformationTarget",
        "SubstanceSourceMaterial",
        "SubstanceSourceMaterialFractionDescription",
        "SubstanceSourceMaterialOrganism",
        "SubstanceSourceMaterialOrganismAuthor",
        "SubstanceSourceMaterialOrganismHybrid",
        "SubstanceSourceMaterialOrganismOrganismGeneral",
        "SubstanceSourceMaterialPartDescription",
        "SubstanceSpecification",
        "SubstanceSpecificationCode",
        "SubstanceSpecificationMoiety",
        "SubstanceSpecificationName",
        "SubstanceSpecificationNameOfficial",
        "SubstanceSpecificationProperty",
        "SubstanceSpecificationRelationship",
        "SubstanceSpecificationStructure",
        "SubstanceSpecificationStructureIsotope",
        "SubstanceSpecificationStructureIsotopeMolecularWeight",
        "SubstanceSpecificationStructureRepresentation",
        "SupplyDelivery",
        "SupplyDeliverySuppliedItem",
        "SupplyRequest",
        "SupplyRequestParameter",
        "Task",
        "TaskInput",
        "TaskOutput",
        "TaskRestriction",
        "TerminologyCapabilities",
        "TerminologyCapabilitiesClosure",
        "TerminologyCapabilitiesCodeSystem",
        "TerminologyCapabilitiesCodeSystemVersion",
        "TerminologyCapabilitiesCodeSystemVersionFilter",
        "TerminologyCapabilitiesExpansion",
        "TerminologyCapabilitiesExpansionParameter",
        "TerminologyCapabilitiesImplementation",
        "TerminologyCapabilitiesSoftware",
        "TerminologyCapabilitiesTranslation",
        "TerminologyCapabilitiesValidateCode",
        "TestReport",
        "TestReportParticipant",
        "TestReportSetup",
        "TestReportSetupAction",
        "TestReportSetupActionAssert",
        "TestReportSetupActionOperation",
        "TestReportTeardown",
        "TestReportTeardownAction",
        "TestReportTest",
        "TestReportTestAction",
        "TestScript",
        "TestScriptDestination",
        "TestScriptFixture",
        "TestScriptMetadata",
        "TestScriptMetadataCapability",
        "TestScriptMetadataLink",
        "TestScriptOrigin",
        "TestScriptSetup",
        "TestScriptSetupAction",
        "TestScriptSetupActionAssert",
        "TestScriptSetupActionOperation",
        "TestScriptSetupActionOperationRequestHeader",
        "TestScriptTeardown",
        "TestScriptTeardownAction",
        "TestScriptTest",
        "TestScriptTestAction",
        "TestScriptVariable",
        "Timing",
        "TimingRepeat",
        "TriggerDefinition",
        "UsageContext",
        "User",
        "UserConfiguration",
        "UserConfigurationMenu",
        "UserConfigurationMenuLink",
        "UserConfigurationOption",
        "UserConfigurationSearch",
        "UserSecurityRequest",
        "ValueSet",
        "ValueSetCompose",
        "ValueSetComposeInclude",
        "ValueSetComposeIncludeConcept",
        "ValueSetComposeIncludeConceptDesignation",
        "ValueSetComposeIncludeFilter",
        "ValueSetExpansion",
        "ValueSetExpansionContains",
        "ValueSetExpansionParameter",
        "VerificationResult",
        "VerificationResultAttestation",
        "VerificationResultPrimarySource",
        "VerificationResultValidator",
        "ViewDefinition",
        "ViewDefinitionConstant",
        "ViewDefinitionSelect",
        "ViewDefinitionSelectColumn",
        "ViewDefinitionSelectColumnTag",
        "ViewDefinitionWhere",
        "VisionPrescription",
        "VisionPrescriptionLensSpecification",
        "VisionPrescriptionLensSpecificationPrism",
    ]
else:
    # At runtime: minimal exports (lazy loading handles the rest)
    __all__ = ["Resource"]
