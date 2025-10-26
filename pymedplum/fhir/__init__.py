# Generated FHIR module
# Do not edit manually

# Import classes directly from their respective modules, e.g.:
# from pymedplum.fhir.patient import Patient
# from pymedplum.fhir.organization import Organization

import importlib
from typing import TYPE_CHECKING, Any, Literal

# ResourceType is a Literal of all FHIR resource type strings
ResourceType = Literal["AccessPolicy", "AccessPolicyIpAccessRule", "AccessPolicyResource", "Account", "AccountCoverage", "AccountGuarantor", "ActivityDefinition", "ActivityDefinitionDynamicValue", "ActivityDefinitionParticipant", "Address", "AdverseEvent", "AdverseEventSuspectEntity", "AdverseEventSuspectEntityCausality", "Age", "Agent", "AgentChannel", "AgentSetting", "AllergyIntolerance", "AllergyIntoleranceReaction", "Annotation", "Appointment", "AppointmentParticipant", "AppointmentResponse", "AsyncJob", "Attachment", "AuditEvent", "AuditEventAgent", "AuditEventAgentNetwork", "AuditEventEntity", "AuditEventEntityDetail", "AuditEventSource", "BackboneElement", "Basic", "Binary", "BiologicallyDerivedProduct", "BiologicallyDerivedProductCollection", "BiologicallyDerivedProductManipulation", "BiologicallyDerivedProductProcessing", "BiologicallyDerivedProductStorage", "BodyStructure", "Bot", "BulkDataExport", "BulkDataExportDeleted", "BulkDataExportError", "BulkDataExportOutput", "Bundle", "BundleEntry", "BundleEntryRequest", "BundleEntryResponse", "BundleEntrySearch", "BundleLink", "CapabilityStatement", "CapabilityStatementDocument", "CapabilityStatementImplementation", "CapabilityStatementMessaging", "CapabilityStatementMessagingEndpoint", "CapabilityStatementMessagingSupportedMessage", "CapabilityStatementRest", "CapabilityStatementRestInteraction", "CapabilityStatementRestResource", "CapabilityStatementRestResourceInteraction", "CapabilityStatementRestResourceOperation", "CapabilityStatementRestResourceSearchParam", "CapabilityStatementRestSecurity", "CapabilityStatementSoftware", "CarePlan", "CarePlanActivity", "CarePlanActivityDetail", "CareTeam", "CareTeamParticipant", "CatalogEntry", "CatalogEntryRelatedEntry", "ChargeItem", "ChargeItemDefinition", "ChargeItemDefinitionApplicability", "ChargeItemDefinitionPropertyGroup", "ChargeItemDefinitionPropertyGroupPriceComponent", "ChargeItemPerformer", "Claim", "ClaimAccident", "ClaimCareTeam", "ClaimDiagnosis", "ClaimInsurance", "ClaimItem", "ClaimItemDetail", "ClaimItemDetailSubDetail", "ClaimPayee", "ClaimProcedure", "ClaimRelated", "ClaimResponse", "ClaimResponseAddItem", "ClaimResponseAddItemDetail", "ClaimResponseAddItemDetailSubDetail", "ClaimResponseError", "ClaimResponseInsurance", "ClaimResponseItem", "ClaimResponseItemAdjudication", "ClaimResponseItemDetail", "ClaimResponseItemDetailSubDetail", "ClaimResponsePayment", "ClaimResponseProcessNote", "ClaimResponseTotal", "ClaimSupportingInfo", "ClientApplication", "ClientApplicationSignInForm", "ClinicalImpression", "ClinicalImpressionFinding", "ClinicalImpressionInvestigation", "CodeSystem", "CodeSystemConcept", "CodeSystemConceptDesignation", "CodeSystemConceptProperty", "CodeSystemFilter", "CodeSystemProperty", "CodeableConcept", "Coding", "Communication", "CommunicationPayload", "CommunicationRequest", "CommunicationRequestPayload", "CompartmentDefinition", "CompartmentDefinitionResource", "Composition", "CompositionAttester", "CompositionEvent", "CompositionRelatesTo", "CompositionSection", "ConceptMap", "ConceptMapGroup", "ConceptMapGroupElement", "ConceptMapGroupElementTarget", "ConceptMapGroupElementTargetDependsOn", "ConceptMapGroupUnmapped", "Condition", "ConditionEvidence", "ConditionStage", "Consent", "ConsentPolicy", "ConsentProvision", "ConsentProvisionActor", "ConsentProvisionData", "ConsentVerification", "ContactDetail", "ContactPoint", "Contract", "ContractContentDefinition", "ContractFriendly", "ContractLegal", "ContractRule", "ContractSigner", "ContractTerm", "ContractTermAction", "ContractTermActionSubject", "ContractTermAsset", "ContractTermAssetContext", "ContractTermAssetValuedItem", "ContractTermOffer", "ContractTermOfferAnswer", "ContractTermOfferParty", "ContractTermSecurityLabel", "Contributor", "Count", "Coverage", "CoverageClass", "CoverageCostToBeneficiary", "CoverageCostToBeneficiaryException", "CoverageEligibilityRequest", "CoverageEligibilityRequestInsurance", "CoverageEligibilityRequestItem", "CoverageEligibilityRequestItemDiagnosis", "CoverageEligibilityRequestSupportingInfo", "CoverageEligibilityResponse", "CoverageEligibilityResponseError", "CoverageEligibilityResponseInsurance", "CoverageEligibilityResponseInsuranceItem", "CoverageEligibilityResponseInsuranceItemBenefit", "DataRequirement", "DataRequirementCodeFilter", "DataRequirementDateFilter", "DataRequirementSort", "DetectedIssue", "DetectedIssueEvidence", "DetectedIssueMitigation", "Device", "DeviceDefinition", "DeviceDefinitionCapability", "DeviceDefinitionClassification", "DeviceDefinitionDeviceName", "DeviceDefinitionMaterial", "DeviceDefinitionProperty", "DeviceDefinitionSpecialization", "DeviceDefinitionUdiDeviceIdentifier", "DeviceDeviceName", "DeviceMetric", "DeviceMetricCalibration", "DeviceProperty", "DeviceRequest", "DeviceRequestParameter", "DeviceSpecialization", "DeviceUdiCarrier", "DeviceUseStatement", "DeviceVersion", "DiagnosticReport", "DiagnosticReportMedia", "Distance", "DocumentManifest", "DocumentManifestRelated", "DocumentReference", "DocumentReferenceContent", "DocumentReferenceContext", "DocumentReferenceRelatesTo", "DomainConfiguration", "Dosage", "DosageDoseAndRate", "Duration", "EffectEvidenceSynthesis", "EffectEvidenceSynthesisCertainty", "EffectEvidenceSynthesisCertaintyCertaintySubcomponent", "EffectEvidenceSynthesisEffectEstimate", "EffectEvidenceSynthesisEffectEstimatePrecisionEstimate", "EffectEvidenceSynthesisResultsByExposure", "EffectEvidenceSynthesisSampleSize", "Element", "ElementDefinition", "ElementDefinitionBase", "ElementDefinitionBinding", "ElementDefinitionConstraint", "ElementDefinitionExample", "ElementDefinitionMapping", "ElementDefinitionSlicing", "ElementDefinitionSlicingDiscriminator", "ElementDefinitionType", "Encounter", "EncounterClassHistory", "EncounterDiagnosis", "EncounterHospitalization", "EncounterLocation", "EncounterParticipant", "EncounterStatusHistory", "Endpoint", "EnrollmentRequest", "EnrollmentResponse", "EpisodeOfCare", "EpisodeOfCareDiagnosis", "EpisodeOfCareStatusHistory", "EventDefinition", "Evidence", "EvidenceVariable", "EvidenceVariableCharacteristic", "EvidenceVariableCharacteristicDefinitionByCombination", "EvidenceVariableCharacteristicDefinitionByTypeAndValue", "EvidenceVariableCharacteristicTimeFromEvent", "ExampleScenario", "ExampleScenarioActor", "ExampleScenarioInstance", "ExampleScenarioInstanceContainedInstance", "ExampleScenarioInstanceVersion", "ExampleScenarioProcess", "ExampleScenarioProcessStep", "ExampleScenarioProcessStepAlternative", "ExampleScenarioProcessStepOperation", "ExplanationOfBenefit", "ExplanationOfBenefitAccident", "ExplanationOfBenefitAddItem", "ExplanationOfBenefitAddItemDetail", "ExplanationOfBenefitAddItemDetailSubDetail", "ExplanationOfBenefitBenefitBalance", "ExplanationOfBenefitBenefitBalanceFinancial", "ExplanationOfBenefitCareTeam", "ExplanationOfBenefitDiagnosis", "ExplanationOfBenefitInsurance", "ExplanationOfBenefitItem", "ExplanationOfBenefitItemAdjudication", "ExplanationOfBenefitItemDetail", "ExplanationOfBenefitItemDetailSubDetail", "ExplanationOfBenefitPayee", "ExplanationOfBenefitPayment", "ExplanationOfBenefitProcedure", "ExplanationOfBenefitProcessNote", "ExplanationOfBenefitRelated", "ExplanationOfBenefitSupportingInfo", "ExplanationOfBenefitTotal", "Expression", "Extension", "FamilyMemberHistory", "FamilyMemberHistoryCondition", "Flag", "Goal", "GoalTarget", "GraphDefinition", "GraphDefinitionLink", "GraphDefinitionLinkTarget", "GraphDefinitionLinkTargetCompartment", "Group", "GroupCharacteristic", "GroupMember", "GuidanceResponse", "HealthcareService", "HealthcareServiceAvailableTime", "HealthcareServiceEligibility", "HealthcareServiceNotAvailable", "HumanName", "Identifier", "IdentityProvider", "ImagingStudy", "ImagingStudySeries", "ImagingStudySeriesInstance", "ImagingStudySeriesPerformer", "Immunization", "ImmunizationEducation", "ImmunizationEvaluation", "ImmunizationPerformer", "ImmunizationProtocolApplied", "ImmunizationReaction", "ImmunizationRecommendation", "ImmunizationRecommendationRecommendation", "ImmunizationRecommendationRecommendationDateCriterion", "ImplementationGuide", "ImplementationGuideDefinition", "ImplementationGuideDefinitionGrouping", "ImplementationGuideDefinitionPage", "ImplementationGuideDefinitionParameter", "ImplementationGuideDefinitionResource", "ImplementationGuideDefinitionTemplate", "ImplementationGuideDependsOn", "ImplementationGuideGlobal", "ImplementationGuideManifest", "ImplementationGuideManifestPage", "ImplementationGuideManifestResource", "InsurancePlan", "InsurancePlanContact", "InsurancePlanCoverage", "InsurancePlanCoverageBenefit", "InsurancePlanCoverageBenefitLimit", "InsurancePlanPlan", "InsurancePlanPlanGeneralCost", "InsurancePlanPlanSpecificCost", "InsurancePlanPlanSpecificCostBenefit", "InsurancePlanPlanSpecificCostBenefitCost", "Invoice", "InvoiceLineItem", "InvoiceLineItemPriceComponent", "InvoiceParticipant", "JsonWebKey", "Library", "Linkage", "LinkageItem", "List", "ListEntry", "Location", "LocationHoursOfOperation", "LocationPosition", "Login", "MarketingStatus", "Measure", "MeasureGroup", "MeasureGroupPopulation", "MeasureGroupStratifier", "MeasureGroupStratifierComponent", "MeasureReport", "MeasureReportGroup", "MeasureReportGroupPopulation", "MeasureReportGroupStratifier", "MeasureReportGroupStratifierStratum", "MeasureReportGroupStratifierStratumComponent", "MeasureReportGroupStratifierStratumPopulation", "MeasureSupplementalData", "Media", "Medication", "MedicationAdministration", "MedicationAdministrationDosage", "MedicationAdministrationPerformer", "MedicationBatch", "MedicationDispense", "MedicationDispensePerformer", "MedicationDispenseSubstitution", "MedicationIngredient", "MedicationKnowledge", "MedicationKnowledgeAdministrationGuidelines", "MedicationKnowledgeAdministrationGuidelinesDosage", "MedicationKnowledgeAdministrationGuidelinesPatientCharacteristics", "MedicationKnowledgeCost", "MedicationKnowledgeDrugCharacteristic", "MedicationKnowledgeIngredient", "MedicationKnowledgeKinetics", "MedicationKnowledgeMedicineClassification", "MedicationKnowledgeMonitoringProgram", "MedicationKnowledgeMonograph", "MedicationKnowledgePackaging", "MedicationKnowledgeRegulatory", "MedicationKnowledgeRegulatoryMaxDispense", "MedicationKnowledgeRegulatorySchedule", "MedicationKnowledgeRegulatorySubstitution", "MedicationKnowledgeRelatedMedicationKnowledge", "MedicationRequest", "MedicationRequestDispenseRequest", "MedicationRequestDispenseRequestInitialFill", "MedicationRequestSubstitution", "MedicationStatement", "MedicinalProduct", "MedicinalProductAuthorization", "MedicinalProductAuthorizationJurisdictionalAuthorization", "MedicinalProductAuthorizationProcedure", "MedicinalProductContraindication", "MedicinalProductContraindicationOtherTherapy", "MedicinalProductIndication", "MedicinalProductIndicationOtherTherapy", "MedicinalProductIngredient", "MedicinalProductIngredientSpecifiedSubstance", "MedicinalProductIngredientSpecifiedSubstanceStrength", "MedicinalProductIngredientSpecifiedSubstanceStrengthReferenceStrength", "MedicinalProductIngredientSubstance", "MedicinalProductInteraction", "MedicinalProductInteractionInteractant", "MedicinalProductManufactured", "MedicinalProductManufacturingBusinessOperation", "MedicinalProductName", "MedicinalProductNameCountryLanguage", "MedicinalProductNameNamePart", "MedicinalProductPackaged", "MedicinalProductPackagedBatchIdentifier", "MedicinalProductPackagedPackageItem", "MedicinalProductPharmaceutical", "MedicinalProductPharmaceuticalCharacteristics", "MedicinalProductPharmaceuticalRouteOfAdministration", "MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpecies", "MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpeciesWithdrawalPeriod", "MedicinalProductSpecialDesignation", "MedicinalProductUndesirableEffect", "MessageDefinition", "MessageDefinitionAllowedResponse", "MessageDefinitionFocus", "MessageHeader", "MessageHeaderDestination", "MessageHeaderResponse", "MessageHeaderSource", "Meta", "MetadataResource", "MolecularSequence", "MolecularSequenceQuality", "MolecularSequenceQualityRoc", "MolecularSequenceReferenceSeq", "MolecularSequenceRepository", "MolecularSequenceStructureVariant", "MolecularSequenceStructureVariantInner", "MolecularSequenceStructureVariantOuter", "MolecularSequenceVariant", "Money", "MoneyQuantity", "NamingSystem", "NamingSystemUniqueId", "Narrative", "NutritionOrder", "NutritionOrderEnteralFormula", "NutritionOrderEnteralFormulaAdministration", "NutritionOrderOralDiet", "NutritionOrderOralDietNutrient", "NutritionOrderOralDietTexture", "NutritionOrderSupplement", "Observation", "ObservationComponent", "ObservationDefinition", "ObservationDefinitionQualifiedInterval", "ObservationDefinitionQuantitativeDetails", "ObservationReferenceRange", "OperationDefinition", "OperationDefinitionOverload", "OperationDefinitionParameter", "OperationDefinitionParameterBinding", "OperationDefinitionParameterReferencedFrom", "OperationOutcome", "OperationOutcomeIssue", "Organization", "OrganizationAffiliation", "OrganizationContact", "ParameterDefinition", "Parameters", "ParametersParameter", "PasswordChangeRequest", "Patient", "PatientCommunication", "PatientContact", "PatientLink", "PaymentNotice", "PaymentReconciliation", "PaymentReconciliationDetail", "PaymentReconciliationProcessNote", "Period", "Person", "PersonLink", "PlanDefinition", "PlanDefinitionAction", "PlanDefinitionActionCondition", "PlanDefinitionActionDynamicValue", "PlanDefinitionActionParticipant", "PlanDefinitionActionRelatedAction", "PlanDefinitionGoal", "PlanDefinitionGoalTarget", "Population", "Practitioner", "PractitionerQualification", "PractitionerRole", "PractitionerRoleAvailableTime", "PractitionerRoleNotAvailable", "Procedure", "ProcedureFocalDevice", "ProcedurePerformer", "ProdCharacteristic", "ProductShelfLife", "Project", "ProjectDefaultProfile", "ProjectLink", "ProjectMembership", "ProjectMembershipAccess", "ProjectMembershipAccessParameter", "ProjectSetting", "ProjectSite", "Provenance", "ProvenanceAgent", "ProvenanceEntity", "Quantity", "Questionnaire", "QuestionnaireItem", "QuestionnaireItemAnswerOption", "QuestionnaireItemEnableWhen", "QuestionnaireItemInitial", "QuestionnaireResponse", "QuestionnaireResponseItem", "QuestionnaireResponseItemAnswer", "Range", "Ratio", "Reference", "RelatedArtifact", "RelatedPerson", "RelatedPersonCommunication", "RequestGroup", "RequestGroupAction", "RequestGroupActionCondition", "RequestGroupActionRelatedAction", "ResearchDefinition", "ResearchElementDefinition", "ResearchElementDefinitionCharacteristic", "ResearchStudy", "ResearchStudyArm", "ResearchStudyAssociatedParty", "ResearchStudyComparisonGroup", "ResearchStudyLabel", "ResearchStudyObjective", "ResearchStudyOutcomeMeasure", "ResearchStudyProgressStatus", "ResearchStudyRecruitment", "ResearchSubject", "RiskAssessment", "RiskAssessmentPrediction", "RiskEvidenceSynthesis", "RiskEvidenceSynthesisCertainty", "RiskEvidenceSynthesisCertaintyCertaintySubcomponent", "RiskEvidenceSynthesisRiskEstimate", "RiskEvidenceSynthesisRiskEstimatePrecisionEstimate", "RiskEvidenceSynthesisSampleSize", "SampledData", "Schedule", "SearchParameter", "SearchParameterComponent", "ServiceRequest", "Signature", "SimpleQuantity", "Slot", "SmartAppLaunch", "Specimen", "SpecimenCollection", "SpecimenContainer", "SpecimenDefinition", "SpecimenDefinitionTypeTested", "SpecimenDefinitionTypeTestedContainer", "SpecimenDefinitionTypeTestedContainerAdditive", "SpecimenDefinitionTypeTestedHandling", "SpecimenProcessing", "StructureDefinition", "StructureDefinitionContext", "StructureDefinitionDifferential", "StructureDefinitionMapping", "StructureDefinitionSnapshot", "StructureMap", "StructureMapGroup", "StructureMapGroupInput", "StructureMapGroupRule", "StructureMapGroupRuleDependent", "StructureMapGroupRuleSource", "StructureMapGroupRuleTarget", "StructureMapGroupRuleTargetParameter", "StructureMapStructure", "Subscription", "SubscriptionChannel", "SubscriptionStatus", "SubscriptionStatusNotificationEvent", "Substance", "SubstanceAmount", "SubstanceAmountReferenceRange", "SubstanceIngredient", "SubstanceInstance", "SubstanceNucleicAcid", "SubstanceNucleicAcidSubunit", "SubstanceNucleicAcidSubunitLinkage", "SubstanceNucleicAcidSubunitSugar", "SubstancePolymer", "SubstancePolymerMonomerSet", "SubstancePolymerMonomerSetStartingMaterial", "SubstancePolymerRepeat", "SubstancePolymerRepeatRepeatUnit", "SubstancePolymerRepeatRepeatUnitDegreeOfPolymerisation", "SubstancePolymerRepeatRepeatUnitStructuralRepresentation", "SubstanceProtein", "SubstanceProteinSubunit", "SubstanceReferenceInformation", "SubstanceReferenceInformationClassification", "SubstanceReferenceInformationGene", "SubstanceReferenceInformationGeneElement", "SubstanceReferenceInformationTarget", "SubstanceSourceMaterial", "SubstanceSourceMaterialFractionDescription", "SubstanceSourceMaterialOrganism", "SubstanceSourceMaterialOrganismAuthor", "SubstanceSourceMaterialOrganismHybrid", "SubstanceSourceMaterialOrganismOrganismGeneral", "SubstanceSourceMaterialPartDescription", "SubstanceSpecification", "SubstanceSpecificationCode", "SubstanceSpecificationMoiety", "SubstanceSpecificationName", "SubstanceSpecificationNameOfficial", "SubstanceSpecificationProperty", "SubstanceSpecificationRelationship", "SubstanceSpecificationStructure", "SubstanceSpecificationStructureIsotope", "SubstanceSpecificationStructureIsotopeMolecularWeight", "SubstanceSpecificationStructureRepresentation", "SupplyDelivery", "SupplyDeliverySuppliedItem", "SupplyRequest", "SupplyRequestParameter", "Task", "TaskInput", "TaskOutput", "TaskRestriction", "TerminologyCapabilities", "TerminologyCapabilitiesClosure", "TerminologyCapabilitiesCodeSystem", "TerminologyCapabilitiesCodeSystemVersion", "TerminologyCapabilitiesCodeSystemVersionFilter", "TerminologyCapabilitiesExpansion", "TerminologyCapabilitiesExpansionParameter", "TerminologyCapabilitiesImplementation", "TerminologyCapabilitiesSoftware", "TerminologyCapabilitiesTranslation", "TerminologyCapabilitiesValidateCode", "TestReport", "TestReportParticipant", "TestReportSetup", "TestReportSetupAction", "TestReportSetupActionAssert", "TestReportSetupActionOperation", "TestReportTeardown", "TestReportTeardownAction", "TestReportTest", "TestReportTestAction", "TestScript", "TestScriptDestination", "TestScriptFixture", "TestScriptMetadata", "TestScriptMetadataCapability", "TestScriptMetadataLink", "TestScriptOrigin", "TestScriptSetup", "TestScriptSetupAction", "TestScriptSetupActionAssert", "TestScriptSetupActionOperation", "TestScriptSetupActionOperationRequestHeader", "TestScriptTeardown", "TestScriptTeardownAction", "TestScriptTest", "TestScriptTestAction", "TestScriptVariable", "Timing", "TimingRepeat", "TriggerDefinition", "UsageContext", "User", "UserConfiguration", "UserConfigurationMenu", "UserConfigurationMenuLink", "UserConfigurationOption", "UserConfigurationSearch", "UserSecurityRequest", "ValueSet", "ValueSetCompose", "ValueSetComposeInclude", "ValueSetComposeIncludeConcept", "ValueSetComposeIncludeConceptDesignation", "ValueSetComposeIncludeFilter", "ValueSetExpansion", "ValueSetExpansionContains", "ValueSetExpansionParameter", "VerificationResult", "VerificationResultAttestation", "VerificationResultPrimarySource", "VerificationResultValidator", "ViewDefinition", "ViewDefinitionConstant", "ViewDefinitionSelect", "ViewDefinitionSelectColumn", "ViewDefinitionSelectColumnTag", "ViewDefinitionWhere", "VisionPrescription", "VisionPrescriptionLensSpecification", "VisionPrescriptionLensSpecificationPrism"]

if TYPE_CHECKING:
    # Resource is a union of all FHIR resource types
    # Import all resources for type checking
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

    Resource = AccessPolicy | AccessPolicyIpAccessRule | AccessPolicyResource | Account | AccountCoverage | AccountGuarantor | ActivityDefinition | ActivityDefinitionDynamicValue | ActivityDefinitionParticipant | Address | AdverseEvent | AdverseEventSuspectEntity | AdverseEventSuspectEntityCausality | Age | Agent | AgentChannel | AgentSetting | AllergyIntolerance | AllergyIntoleranceReaction | Annotation | Appointment | AppointmentParticipant | AppointmentResponse | AsyncJob | Attachment | AuditEvent | AuditEventAgent | AuditEventAgentNetwork | AuditEventEntity | AuditEventEntityDetail | AuditEventSource | BackboneElement | Basic | Binary | BiologicallyDerivedProduct | BiologicallyDerivedProductCollection | BiologicallyDerivedProductManipulation | BiologicallyDerivedProductProcessing | BiologicallyDerivedProductStorage | BodyStructure | Bot | BulkDataExport | BulkDataExportDeleted | BulkDataExportError | BulkDataExportOutput | Bundle | BundleEntry | BundleEntryRequest | BundleEntryResponse | BundleEntrySearch | BundleLink | CapabilityStatement | CapabilityStatementDocument | CapabilityStatementImplementation | CapabilityStatementMessaging | CapabilityStatementMessagingEndpoint | CapabilityStatementMessagingSupportedMessage | CapabilityStatementRest | CapabilityStatementRestInteraction | CapabilityStatementRestResource | CapabilityStatementRestResourceInteraction | CapabilityStatementRestResourceOperation | CapabilityStatementRestResourceSearchParam | CapabilityStatementRestSecurity | CapabilityStatementSoftware | CarePlan | CarePlanActivity | CarePlanActivityDetail | CareTeam | CareTeamParticipant | CatalogEntry | CatalogEntryRelatedEntry | ChargeItem | ChargeItemDefinition | ChargeItemDefinitionApplicability | ChargeItemDefinitionPropertyGroup | ChargeItemDefinitionPropertyGroupPriceComponent | ChargeItemPerformer | Claim | ClaimAccident | ClaimCareTeam | ClaimDiagnosis | ClaimInsurance | ClaimItem | ClaimItemDetail | ClaimItemDetailSubDetail | ClaimPayee | ClaimProcedure | ClaimRelated | ClaimResponse | ClaimResponseAddItem | ClaimResponseAddItemDetail | ClaimResponseAddItemDetailSubDetail | ClaimResponseError | ClaimResponseInsurance | ClaimResponseItem | ClaimResponseItemAdjudication | ClaimResponseItemDetail | ClaimResponseItemDetailSubDetail | ClaimResponsePayment | ClaimResponseProcessNote | ClaimResponseTotal | ClaimSupportingInfo | ClientApplication | ClientApplicationSignInForm | ClinicalImpression | ClinicalImpressionFinding | ClinicalImpressionInvestigation | CodeSystem | CodeSystemConcept | CodeSystemConceptDesignation | CodeSystemConceptProperty | CodeSystemFilter | CodeSystemProperty | CodeableConcept | Coding | Communication | CommunicationPayload | CommunicationRequest | CommunicationRequestPayload | CompartmentDefinition | CompartmentDefinitionResource | Composition | CompositionAttester | CompositionEvent | CompositionRelatesTo | CompositionSection | ConceptMap | ConceptMapGroup | ConceptMapGroupElement | ConceptMapGroupElementTarget | ConceptMapGroupElementTargetDependsOn | ConceptMapGroupUnmapped | Condition | ConditionEvidence | ConditionStage | Consent | ConsentPolicy | ConsentProvision | ConsentProvisionActor | ConsentProvisionData | ConsentVerification | ContactDetail | ContactPoint | Contract | ContractContentDefinition | ContractFriendly | ContractLegal | ContractRule | ContractSigner | ContractTerm | ContractTermAction | ContractTermActionSubject | ContractTermAsset | ContractTermAssetContext | ContractTermAssetValuedItem | ContractTermOffer | ContractTermOfferAnswer | ContractTermOfferParty | ContractTermSecurityLabel | Contributor | Count | Coverage | CoverageClass | CoverageCostToBeneficiary | CoverageCostToBeneficiaryException | CoverageEligibilityRequest | CoverageEligibilityRequestInsurance | CoverageEligibilityRequestItem | CoverageEligibilityRequestItemDiagnosis | CoverageEligibilityRequestSupportingInfo | CoverageEligibilityResponse | CoverageEligibilityResponseError | CoverageEligibilityResponseInsurance | CoverageEligibilityResponseInsuranceItem | CoverageEligibilityResponseInsuranceItemBenefit | DataRequirement | DataRequirementCodeFilter | DataRequirementDateFilter | DataRequirementSort | DetectedIssue | DetectedIssueEvidence | DetectedIssueMitigation | Device | DeviceDefinition | DeviceDefinitionCapability | DeviceDefinitionClassification | DeviceDefinitionDeviceName | DeviceDefinitionMaterial | DeviceDefinitionProperty | DeviceDefinitionSpecialization | DeviceDefinitionUdiDeviceIdentifier | DeviceDeviceName | DeviceMetric | DeviceMetricCalibration | DeviceProperty | DeviceRequest | DeviceRequestParameter | DeviceSpecialization | DeviceUdiCarrier | DeviceUseStatement | DeviceVersion | DiagnosticReport | DiagnosticReportMedia | Distance | DocumentManifest | DocumentManifestRelated | DocumentReference | DocumentReferenceContent | DocumentReferenceContext | DocumentReferenceRelatesTo | DomainConfiguration | Dosage | DosageDoseAndRate | Duration | EffectEvidenceSynthesis | EffectEvidenceSynthesisCertainty | EffectEvidenceSynthesisCertaintyCertaintySubcomponent | EffectEvidenceSynthesisEffectEstimate | EffectEvidenceSynthesisEffectEstimatePrecisionEstimate | EffectEvidenceSynthesisResultsByExposure | EffectEvidenceSynthesisSampleSize | Element | ElementDefinition | ElementDefinitionBase | ElementDefinitionBinding | ElementDefinitionConstraint | ElementDefinitionExample | ElementDefinitionMapping | ElementDefinitionSlicing | ElementDefinitionSlicingDiscriminator | ElementDefinitionType | Encounter | EncounterClassHistory | EncounterDiagnosis | EncounterHospitalization | EncounterLocation | EncounterParticipant | EncounterStatusHistory | Endpoint | EnrollmentRequest | EnrollmentResponse | EpisodeOfCare | EpisodeOfCareDiagnosis | EpisodeOfCareStatusHistory | EventDefinition | Evidence | EvidenceVariable | EvidenceVariableCharacteristic | EvidenceVariableCharacteristicDefinitionByCombination | EvidenceVariableCharacteristicDefinitionByTypeAndValue | EvidenceVariableCharacteristicTimeFromEvent | ExampleScenario | ExampleScenarioActor | ExampleScenarioInstance | ExampleScenarioInstanceContainedInstance | ExampleScenarioInstanceVersion | ExampleScenarioProcess | ExampleScenarioProcessStep | ExampleScenarioProcessStepAlternative | ExampleScenarioProcessStepOperation | ExplanationOfBenefit | ExplanationOfBenefitAccident | ExplanationOfBenefitAddItem | ExplanationOfBenefitAddItemDetail | ExplanationOfBenefitAddItemDetailSubDetail | ExplanationOfBenefitBenefitBalance | ExplanationOfBenefitBenefitBalanceFinancial | ExplanationOfBenefitCareTeam | ExplanationOfBenefitDiagnosis | ExplanationOfBenefitInsurance | ExplanationOfBenefitItem | ExplanationOfBenefitItemAdjudication | ExplanationOfBenefitItemDetail | ExplanationOfBenefitItemDetailSubDetail | ExplanationOfBenefitPayee | ExplanationOfBenefitPayment | ExplanationOfBenefitProcedure | ExplanationOfBenefitProcessNote | ExplanationOfBenefitRelated | ExplanationOfBenefitSupportingInfo | ExplanationOfBenefitTotal | Expression | Extension | FamilyMemberHistory | FamilyMemberHistoryCondition | Flag | Goal | GoalTarget | GraphDefinition | GraphDefinitionLink | GraphDefinitionLinkTarget | GraphDefinitionLinkTargetCompartment | Group | GroupCharacteristic | GroupMember | GuidanceResponse | HealthcareService | HealthcareServiceAvailableTime | HealthcareServiceEligibility | HealthcareServiceNotAvailable | HumanName | Identifier | IdentityProvider | ImagingStudy | ImagingStudySeries | ImagingStudySeriesInstance | ImagingStudySeriesPerformer | Immunization | ImmunizationEducation | ImmunizationEvaluation | ImmunizationPerformer | ImmunizationProtocolApplied | ImmunizationReaction | ImmunizationRecommendation | ImmunizationRecommendationRecommendation | ImmunizationRecommendationRecommendationDateCriterion | ImplementationGuide | ImplementationGuideDefinition | ImplementationGuideDefinitionGrouping | ImplementationGuideDefinitionPage | ImplementationGuideDefinitionParameter | ImplementationGuideDefinitionResource | ImplementationGuideDefinitionTemplate | ImplementationGuideDependsOn | ImplementationGuideGlobal | ImplementationGuideManifest | ImplementationGuideManifestPage | ImplementationGuideManifestResource | InsurancePlan | InsurancePlanContact | InsurancePlanCoverage | InsurancePlanCoverageBenefit | InsurancePlanCoverageBenefitLimit | InsurancePlanPlan | InsurancePlanPlanGeneralCost | InsurancePlanPlanSpecificCost | InsurancePlanPlanSpecificCostBenefit | InsurancePlanPlanSpecificCostBenefitCost | Invoice | InvoiceLineItem | InvoiceLineItemPriceComponent | InvoiceParticipant | JsonWebKey | Library | Linkage | LinkageItem | List | ListEntry | Location | LocationHoursOfOperation | LocationPosition | Login | MarketingStatus | Measure | MeasureGroup | MeasureGroupPopulation | MeasureGroupStratifier | MeasureGroupStratifierComponent | MeasureReport | MeasureReportGroup | MeasureReportGroupPopulation | MeasureReportGroupStratifier | MeasureReportGroupStratifierStratum | MeasureReportGroupStratifierStratumComponent | MeasureReportGroupStratifierStratumPopulation | MeasureSupplementalData | Media | Medication | MedicationAdministration | MedicationAdministrationDosage | MedicationAdministrationPerformer | MedicationBatch | MedicationDispense | MedicationDispensePerformer | MedicationDispenseSubstitution | MedicationIngredient | MedicationKnowledge | MedicationKnowledgeAdministrationGuidelines | MedicationKnowledgeAdministrationGuidelinesDosage | MedicationKnowledgeAdministrationGuidelinesPatientCharacteristics | MedicationKnowledgeCost | MedicationKnowledgeDrugCharacteristic | MedicationKnowledgeIngredient | MedicationKnowledgeKinetics | MedicationKnowledgeMedicineClassification | MedicationKnowledgeMonitoringProgram | MedicationKnowledgeMonograph | MedicationKnowledgePackaging | MedicationKnowledgeRegulatory | MedicationKnowledgeRegulatoryMaxDispense | MedicationKnowledgeRegulatorySchedule | MedicationKnowledgeRegulatorySubstitution | MedicationKnowledgeRelatedMedicationKnowledge | MedicationRequest | MedicationRequestDispenseRequest | MedicationRequestDispenseRequestInitialFill | MedicationRequestSubstitution | MedicationStatement | MedicinalProduct | MedicinalProductAuthorization | MedicinalProductAuthorizationJurisdictionalAuthorization | MedicinalProductAuthorizationProcedure | MedicinalProductContraindication | MedicinalProductContraindicationOtherTherapy | MedicinalProductIndication | MedicinalProductIndicationOtherTherapy | MedicinalProductIngredient | MedicinalProductIngredientSpecifiedSubstance | MedicinalProductIngredientSpecifiedSubstanceStrength | MedicinalProductIngredientSpecifiedSubstanceStrengthReferenceStrength | MedicinalProductIngredientSubstance | MedicinalProductInteraction | MedicinalProductInteractionInteractant | MedicinalProductManufactured | MedicinalProductManufacturingBusinessOperation | MedicinalProductName | MedicinalProductNameCountryLanguage | MedicinalProductNameNamePart | MedicinalProductPackaged | MedicinalProductPackagedBatchIdentifier | MedicinalProductPackagedPackageItem | MedicinalProductPharmaceutical | MedicinalProductPharmaceuticalCharacteristics | MedicinalProductPharmaceuticalRouteOfAdministration | MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpecies | MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpeciesWithdrawalPeriod | MedicinalProductSpecialDesignation | MedicinalProductUndesirableEffect | MessageDefinition | MessageDefinitionAllowedResponse | MessageDefinitionFocus | MessageHeader | MessageHeaderDestination | MessageHeaderResponse | MessageHeaderSource | Meta | MetadataResource | MolecularSequence | MolecularSequenceQuality | MolecularSequenceQualityRoc | MolecularSequenceReferenceSeq | MolecularSequenceRepository | MolecularSequenceStructureVariant | MolecularSequenceStructureVariantInner | MolecularSequenceStructureVariantOuter | MolecularSequenceVariant | Money | MoneyQuantity | NamingSystem | NamingSystemUniqueId | Narrative | NutritionOrder | NutritionOrderEnteralFormula | NutritionOrderEnteralFormulaAdministration | NutritionOrderOralDiet | NutritionOrderOralDietNutrient | NutritionOrderOralDietTexture | NutritionOrderSupplement | Observation | ObservationComponent | ObservationDefinition | ObservationDefinitionQualifiedInterval | ObservationDefinitionQuantitativeDetails | ObservationReferenceRange | OperationDefinition | OperationDefinitionOverload | OperationDefinitionParameter | OperationDefinitionParameterBinding | OperationDefinitionParameterReferencedFrom | OperationOutcome | OperationOutcomeIssue | Organization | OrganizationAffiliation | OrganizationContact | ParameterDefinition | Parameters | ParametersParameter | PasswordChangeRequest | Patient | PatientCommunication | PatientContact | PatientLink | PaymentNotice | PaymentReconciliation | PaymentReconciliationDetail | PaymentReconciliationProcessNote | Period | Person | PersonLink | PlanDefinition | PlanDefinitionAction | PlanDefinitionActionCondition | PlanDefinitionActionDynamicValue | PlanDefinitionActionParticipant | PlanDefinitionActionRelatedAction | PlanDefinitionGoal | PlanDefinitionGoalTarget | Population | Practitioner | PractitionerQualification | PractitionerRole | PractitionerRoleAvailableTime | PractitionerRoleNotAvailable | Procedure | ProcedureFocalDevice | ProcedurePerformer | ProdCharacteristic | ProductShelfLife | Project | ProjectDefaultProfile | ProjectLink | ProjectMembership | ProjectMembershipAccess | ProjectMembershipAccessParameter | ProjectSetting | ProjectSite | Provenance | ProvenanceAgent | ProvenanceEntity | Quantity | Questionnaire | QuestionnaireItem | QuestionnaireItemAnswerOption | QuestionnaireItemEnableWhen | QuestionnaireItemInitial | QuestionnaireResponse | QuestionnaireResponseItem | QuestionnaireResponseItemAnswer | Range | Ratio | Reference | RelatedArtifact | RelatedPerson | RelatedPersonCommunication | RequestGroup | RequestGroupAction | RequestGroupActionCondition | RequestGroupActionRelatedAction | ResearchDefinition | ResearchElementDefinition | ResearchElementDefinitionCharacteristic | ResearchStudy | ResearchStudyArm | ResearchStudyAssociatedParty | ResearchStudyComparisonGroup | ResearchStudyLabel | ResearchStudyObjective | ResearchStudyOutcomeMeasure | ResearchStudyProgressStatus | ResearchStudyRecruitment | ResearchSubject | RiskAssessment | RiskAssessmentPrediction | RiskEvidenceSynthesis | RiskEvidenceSynthesisCertainty | RiskEvidenceSynthesisCertaintyCertaintySubcomponent | RiskEvidenceSynthesisRiskEstimate | RiskEvidenceSynthesisRiskEstimatePrecisionEstimate | RiskEvidenceSynthesisSampleSize | SampledData | Schedule | SearchParameter | SearchParameterComponent | ServiceRequest | Signature | SimpleQuantity | Slot | SmartAppLaunch | Specimen | SpecimenCollection | SpecimenContainer | SpecimenDefinition | SpecimenDefinitionTypeTested | SpecimenDefinitionTypeTestedContainer | SpecimenDefinitionTypeTestedContainerAdditive | SpecimenDefinitionTypeTestedHandling | SpecimenProcessing | StructureDefinition | StructureDefinitionContext | StructureDefinitionDifferential | StructureDefinitionMapping | StructureDefinitionSnapshot | StructureMap | StructureMapGroup | StructureMapGroupInput | StructureMapGroupRule | StructureMapGroupRuleDependent | StructureMapGroupRuleSource | StructureMapGroupRuleTarget | StructureMapGroupRuleTargetParameter | StructureMapStructure | Subscription | SubscriptionChannel | SubscriptionStatus | SubscriptionStatusNotificationEvent | Substance | SubstanceAmount | SubstanceAmountReferenceRange | SubstanceIngredient | SubstanceInstance | SubstanceNucleicAcid | SubstanceNucleicAcidSubunit | SubstanceNucleicAcidSubunitLinkage | SubstanceNucleicAcidSubunitSugar | SubstancePolymer | SubstancePolymerMonomerSet | SubstancePolymerMonomerSetStartingMaterial | SubstancePolymerRepeat | SubstancePolymerRepeatRepeatUnit | SubstancePolymerRepeatRepeatUnitDegreeOfPolymerisation | SubstancePolymerRepeatRepeatUnitStructuralRepresentation | SubstanceProtein | SubstanceProteinSubunit | SubstanceReferenceInformation | SubstanceReferenceInformationClassification | SubstanceReferenceInformationGene | SubstanceReferenceInformationGeneElement | SubstanceReferenceInformationTarget | SubstanceSourceMaterial | SubstanceSourceMaterialFractionDescription | SubstanceSourceMaterialOrganism | SubstanceSourceMaterialOrganismAuthor | SubstanceSourceMaterialOrganismHybrid | SubstanceSourceMaterialOrganismOrganismGeneral | SubstanceSourceMaterialPartDescription | SubstanceSpecification | SubstanceSpecificationCode | SubstanceSpecificationMoiety | SubstanceSpecificationName | SubstanceSpecificationNameOfficial | SubstanceSpecificationProperty | SubstanceSpecificationRelationship | SubstanceSpecificationStructure | SubstanceSpecificationStructureIsotope | SubstanceSpecificationStructureIsotopeMolecularWeight | SubstanceSpecificationStructureRepresentation | SupplyDelivery | SupplyDeliverySuppliedItem | SupplyRequest | SupplyRequestParameter | Task | TaskInput | TaskOutput | TaskRestriction | TerminologyCapabilities | TerminologyCapabilitiesClosure | TerminologyCapabilitiesCodeSystem | TerminologyCapabilitiesCodeSystemVersion | TerminologyCapabilitiesCodeSystemVersionFilter | TerminologyCapabilitiesExpansion | TerminologyCapabilitiesExpansionParameter | TerminologyCapabilitiesImplementation | TerminologyCapabilitiesSoftware | TerminologyCapabilitiesTranslation | TerminologyCapabilitiesValidateCode | TestReport | TestReportParticipant | TestReportSetup | TestReportSetupAction | TestReportSetupActionAssert | TestReportSetupActionOperation | TestReportTeardown | TestReportTeardownAction | TestReportTest | TestReportTestAction | TestScript | TestScriptDestination | TestScriptFixture | TestScriptMetadata | TestScriptMetadataCapability | TestScriptMetadataLink | TestScriptOrigin | TestScriptSetup | TestScriptSetupAction | TestScriptSetupActionAssert | TestScriptSetupActionOperation | TestScriptSetupActionOperationRequestHeader | TestScriptTeardown | TestScriptTeardownAction | TestScriptTest | TestScriptTestAction | TestScriptVariable | Timing | TimingRepeat | TriggerDefinition | UsageContext | User | UserConfiguration | UserConfigurationMenu | UserConfigurationMenuLink | UserConfigurationOption | UserConfigurationSearch | UserSecurityRequest | ValueSet | ValueSetCompose | ValueSetComposeInclude | ValueSetComposeIncludeConcept | ValueSetComposeIncludeConceptDesignation | ValueSetComposeIncludeFilter | ValueSetExpansion | ValueSetExpansionContains | ValueSetExpansionParameter | VerificationResult | VerificationResultAttestation | VerificationResultPrimarySource | VerificationResultValidator | ViewDefinition | ViewDefinitionConstant | ViewDefinitionSelect | ViewDefinitionSelectColumn | ViewDefinitionSelectColumnTag | ViewDefinitionWhere | VisionPrescription | VisionPrescriptionLensSpecification | VisionPrescriptionLensSpecificationPrism
else:
    # At runtime, use Any to avoid circular import issues
    Resource = Any

__all__ = ["Resource", "ResourceType"]

# Import all modules to trigger model registration
importlib.import_module("pymedplum.fhir.accesspolicy")
importlib.import_module("pymedplum.fhir.account")
importlib.import_module("pymedplum.fhir.activitydefinition")
importlib.import_module("pymedplum.fhir.address")
importlib.import_module("pymedplum.fhir.adverseevent")
importlib.import_module("pymedplum.fhir.age")
importlib.import_module("pymedplum.fhir.agent")
importlib.import_module("pymedplum.fhir.allergyintolerance")
importlib.import_module("pymedplum.fhir.annotation")
importlib.import_module("pymedplum.fhir.appointment")
importlib.import_module("pymedplum.fhir.appointmentresponse")
importlib.import_module("pymedplum.fhir.asyncjob")
importlib.import_module("pymedplum.fhir.attachment")
importlib.import_module("pymedplum.fhir.auditevent")
importlib.import_module("pymedplum.fhir.backboneelement")
importlib.import_module("pymedplum.fhir.basic")
importlib.import_module("pymedplum.fhir.binary")
importlib.import_module("pymedplum.fhir.biologicallyderivedproduct")
importlib.import_module("pymedplum.fhir.bodystructure")
importlib.import_module("pymedplum.fhir.bot")
importlib.import_module("pymedplum.fhir.bulkdataexport")
importlib.import_module("pymedplum.fhir.bundle")
importlib.import_module("pymedplum.fhir.capabilitystatement")
importlib.import_module("pymedplum.fhir.careplan")
importlib.import_module("pymedplum.fhir.careteam")
importlib.import_module("pymedplum.fhir.catalogentry")
importlib.import_module("pymedplum.fhir.chargeitem")
importlib.import_module("pymedplum.fhir.chargeitemdefinition")
importlib.import_module("pymedplum.fhir.claim")
importlib.import_module("pymedplum.fhir.claimresponse")
importlib.import_module("pymedplum.fhir.clientapplication")
importlib.import_module("pymedplum.fhir.clinicalimpression")
importlib.import_module("pymedplum.fhir.codeableconcept")
importlib.import_module("pymedplum.fhir.codesystem")
importlib.import_module("pymedplum.fhir.coding")
importlib.import_module("pymedplum.fhir.communication")
importlib.import_module("pymedplum.fhir.communicationrequest")
importlib.import_module("pymedplum.fhir.compartmentdefinition")
importlib.import_module("pymedplum.fhir.composition")
importlib.import_module("pymedplum.fhir.conceptmap")
importlib.import_module("pymedplum.fhir.condition")
importlib.import_module("pymedplum.fhir.consent")
importlib.import_module("pymedplum.fhir.contactdetail")
importlib.import_module("pymedplum.fhir.contactpoint")
importlib.import_module("pymedplum.fhir.contract")
importlib.import_module("pymedplum.fhir.contributor")
importlib.import_module("pymedplum.fhir.count")
importlib.import_module("pymedplum.fhir.coverage")
importlib.import_module("pymedplum.fhir.coverageeligibilityrequest")
importlib.import_module("pymedplum.fhir.coverageeligibilityresponse")
importlib.import_module("pymedplum.fhir.datarequirement")
importlib.import_module("pymedplum.fhir.detectedissue")
importlib.import_module("pymedplum.fhir.device")
importlib.import_module("pymedplum.fhir.devicedefinition")
importlib.import_module("pymedplum.fhir.devicemetric")
importlib.import_module("pymedplum.fhir.devicerequest")
importlib.import_module("pymedplum.fhir.deviceusestatement")
importlib.import_module("pymedplum.fhir.diagnosticreport")
importlib.import_module("pymedplum.fhir.distance")
importlib.import_module("pymedplum.fhir.documentmanifest")
importlib.import_module("pymedplum.fhir.documentreference")
importlib.import_module("pymedplum.fhir.domainconfiguration")
importlib.import_module("pymedplum.fhir.dosage")
importlib.import_module("pymedplum.fhir.duration")
importlib.import_module("pymedplum.fhir.effectevidencesynthesis")
importlib.import_module("pymedplum.fhir.element")
importlib.import_module("pymedplum.fhir.elementdefinition")
importlib.import_module("pymedplum.fhir.encounter")
importlib.import_module("pymedplum.fhir.endpoint")
importlib.import_module("pymedplum.fhir.enrollmentrequest")
importlib.import_module("pymedplum.fhir.enrollmentresponse")
importlib.import_module("pymedplum.fhir.episodeofcare")
importlib.import_module("pymedplum.fhir.eventdefinition")
importlib.import_module("pymedplum.fhir.evidence")
importlib.import_module("pymedplum.fhir.evidencevariable")
importlib.import_module("pymedplum.fhir.examplescenario")
importlib.import_module("pymedplum.fhir.explanationofbenefit")
importlib.import_module("pymedplum.fhir.expression")
importlib.import_module("pymedplum.fhir.extension")
importlib.import_module("pymedplum.fhir.familymemberhistory")
importlib.import_module("pymedplum.fhir.flag")
importlib.import_module("pymedplum.fhir.goal")
importlib.import_module("pymedplum.fhir.graphdefinition")
importlib.import_module("pymedplum.fhir.group")
importlib.import_module("pymedplum.fhir.guidanceresponse")
importlib.import_module("pymedplum.fhir.healthcareservice")
importlib.import_module("pymedplum.fhir.humanname")
importlib.import_module("pymedplum.fhir.identifier")
importlib.import_module("pymedplum.fhir.identityprovider")
importlib.import_module("pymedplum.fhir.imagingstudy")
importlib.import_module("pymedplum.fhir.immunization")
importlib.import_module("pymedplum.fhir.immunizationevaluation")
importlib.import_module("pymedplum.fhir.immunizationrecommendation")
importlib.import_module("pymedplum.fhir.implementationguide")
importlib.import_module("pymedplum.fhir.insuranceplan")
importlib.import_module("pymedplum.fhir.invoice")
importlib.import_module("pymedplum.fhir.jsonwebkey")
importlib.import_module("pymedplum.fhir.library")
importlib.import_module("pymedplum.fhir.linkage")
importlib.import_module("pymedplum.fhir.list")
importlib.import_module("pymedplum.fhir.location")
importlib.import_module("pymedplum.fhir.login")
importlib.import_module("pymedplum.fhir.marketingstatus")
importlib.import_module("pymedplum.fhir.measure")
importlib.import_module("pymedplum.fhir.measurereport")
importlib.import_module("pymedplum.fhir.media")
importlib.import_module("pymedplum.fhir.medication")
importlib.import_module("pymedplum.fhir.medicationadministration")
importlib.import_module("pymedplum.fhir.medicationdispense")
importlib.import_module("pymedplum.fhir.medicationknowledge")
importlib.import_module("pymedplum.fhir.medicationrequest")
importlib.import_module("pymedplum.fhir.medicationstatement")
importlib.import_module("pymedplum.fhir.medicinalproduct")
importlib.import_module("pymedplum.fhir.medicinalproductauthorization")
importlib.import_module("pymedplum.fhir.medicinalproductcontraindication")
importlib.import_module("pymedplum.fhir.medicinalproductindication")
importlib.import_module("pymedplum.fhir.medicinalproductingredient")
importlib.import_module("pymedplum.fhir.medicinalproductinteraction")
importlib.import_module("pymedplum.fhir.medicinalproductmanufactured")
importlib.import_module("pymedplum.fhir.medicinalproductpackaged")
importlib.import_module("pymedplum.fhir.medicinalproductpharmaceutical")
importlib.import_module("pymedplum.fhir.medicinalproductundesirableeffect")
importlib.import_module("pymedplum.fhir.messagedefinition")
importlib.import_module("pymedplum.fhir.messageheader")
importlib.import_module("pymedplum.fhir.meta")
importlib.import_module("pymedplum.fhir.metadataresource")
importlib.import_module("pymedplum.fhir.molecularsequence")
importlib.import_module("pymedplum.fhir.money")
importlib.import_module("pymedplum.fhir.moneyquantity")
importlib.import_module("pymedplum.fhir.namingsystem")
importlib.import_module("pymedplum.fhir.narrative")
importlib.import_module("pymedplum.fhir.nutritionorder")
importlib.import_module("pymedplum.fhir.observation")
importlib.import_module("pymedplum.fhir.observationdefinition")
importlib.import_module("pymedplum.fhir.operationdefinition")
importlib.import_module("pymedplum.fhir.operationoutcome")
importlib.import_module("pymedplum.fhir.organization")
importlib.import_module("pymedplum.fhir.organizationaffiliation")
importlib.import_module("pymedplum.fhir.parameterdefinition")
importlib.import_module("pymedplum.fhir.parameters")
importlib.import_module("pymedplum.fhir.passwordchangerequest")
importlib.import_module("pymedplum.fhir.patient")
importlib.import_module("pymedplum.fhir.paymentnotice")
importlib.import_module("pymedplum.fhir.paymentreconciliation")
importlib.import_module("pymedplum.fhir.period")
importlib.import_module("pymedplum.fhir.person")
importlib.import_module("pymedplum.fhir.plandefinition")
importlib.import_module("pymedplum.fhir.population")
importlib.import_module("pymedplum.fhir.practitioner")
importlib.import_module("pymedplum.fhir.practitionerrole")
importlib.import_module("pymedplum.fhir.procedure")
importlib.import_module("pymedplum.fhir.prodcharacteristic")
importlib.import_module("pymedplum.fhir.productshelflife")
importlib.import_module("pymedplum.fhir.project")
importlib.import_module("pymedplum.fhir.projectmembership")
importlib.import_module("pymedplum.fhir.provenance")
importlib.import_module("pymedplum.fhir.quantity")
importlib.import_module("pymedplum.fhir.questionnaire")
importlib.import_module("pymedplum.fhir.questionnaireresponse")
importlib.import_module("pymedplum.fhir.range")
importlib.import_module("pymedplum.fhir.ratio")
importlib.import_module("pymedplum.fhir.reference")
importlib.import_module("pymedplum.fhir.relatedartifact")
importlib.import_module("pymedplum.fhir.relatedperson")
importlib.import_module("pymedplum.fhir.requestgroup")
importlib.import_module("pymedplum.fhir.researchdefinition")
importlib.import_module("pymedplum.fhir.researchelementdefinition")
importlib.import_module("pymedplum.fhir.researchstudy")
importlib.import_module("pymedplum.fhir.researchsubject")
importlib.import_module("pymedplum.fhir.riskassessment")
importlib.import_module("pymedplum.fhir.riskevidencesynthesis")
importlib.import_module("pymedplum.fhir.sampleddata")
importlib.import_module("pymedplum.fhir.schedule")
importlib.import_module("pymedplum.fhir.searchparameter")
importlib.import_module("pymedplum.fhir.servicerequest")
importlib.import_module("pymedplum.fhir.signature")
importlib.import_module("pymedplum.fhir.simplequantity")
importlib.import_module("pymedplum.fhir.slot")
importlib.import_module("pymedplum.fhir.smartapplaunch")
importlib.import_module("pymedplum.fhir.specimen")
importlib.import_module("pymedplum.fhir.specimendefinition")
importlib.import_module("pymedplum.fhir.structuredefinition")
importlib.import_module("pymedplum.fhir.structuremap")
importlib.import_module("pymedplum.fhir.subscription")
importlib.import_module("pymedplum.fhir.subscriptionstatus")
importlib.import_module("pymedplum.fhir.substance")
importlib.import_module("pymedplum.fhir.substanceamount")
importlib.import_module("pymedplum.fhir.substancenucleicacid")
importlib.import_module("pymedplum.fhir.substancepolymer")
importlib.import_module("pymedplum.fhir.substanceprotein")
importlib.import_module("pymedplum.fhir.substancereferenceinformation")
importlib.import_module("pymedplum.fhir.substancesourcematerial")
importlib.import_module("pymedplum.fhir.substancespecification")
importlib.import_module("pymedplum.fhir.supplydelivery")
importlib.import_module("pymedplum.fhir.supplyrequest")
importlib.import_module("pymedplum.fhir.task")
importlib.import_module("pymedplum.fhir.terminologycapabilities")
importlib.import_module("pymedplum.fhir.testreport")
importlib.import_module("pymedplum.fhir.testscript")
importlib.import_module("pymedplum.fhir.timing")
importlib.import_module("pymedplum.fhir.triggerdefinition")
importlib.import_module("pymedplum.fhir.usagecontext")
importlib.import_module("pymedplum.fhir.user")
importlib.import_module("pymedplum.fhir.userconfiguration")
importlib.import_module("pymedplum.fhir.usersecurityrequest")
importlib.import_module("pymedplum.fhir.valueset")
importlib.import_module("pymedplum.fhir.verificationresult")
importlib.import_module("pymedplum.fhir.viewdefinition")
importlib.import_module("pymedplum.fhir.visionprescription")

# Register special types for forward reference resolution
from pymedplum.fhir._rebuild import rebuild_all_models, register_model  # noqa: E402

register_model('ResourceType', ResourceType)
register_model('Resource', Resource)  # Needed for type resolution even though it's Any at runtime

# Rebuild all models to resolve forward references
rebuild_all_models()
