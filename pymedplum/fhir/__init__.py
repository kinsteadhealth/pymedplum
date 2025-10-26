# Generated FHIR module
# Do not edit manually

# Import classes directly from their respective modules, e.g.:
# from pymedplum.fhir.patient import Patient
# from pymedplum.fhir.organization import Organization

from typing import Any, Literal, TYPE_CHECKING

# ResourceType is a Literal of all FHIR resource type strings
ResourceType = Literal["AccessPolicy", "AccessPolicyIpAccessRule", "AccessPolicyResource", "Account", "AccountCoverage", "AccountGuarantor", "ActivityDefinition", "ActivityDefinitionDynamicValue", "ActivityDefinitionParticipant", "Address", "AdverseEvent", "AdverseEventSuspectEntity", "AdverseEventSuspectEntityCausality", "Age", "Agent", "AgentChannel", "AgentSetting", "AllergyIntolerance", "AllergyIntoleranceReaction", "Annotation", "Appointment", "AppointmentParticipant", "AppointmentResponse", "AsyncJob", "Attachment", "AuditEvent", "AuditEventAgent", "AuditEventAgentNetwork", "AuditEventEntity", "AuditEventEntityDetail", "AuditEventSource", "BackboneElement", "Basic", "Binary", "BiologicallyDerivedProduct", "BiologicallyDerivedProductCollection", "BiologicallyDerivedProductManipulation", "BiologicallyDerivedProductProcessing", "BiologicallyDerivedProductStorage", "BodyStructure", "Bot", "BulkDataExport", "BulkDataExportDeleted", "BulkDataExportError", "BulkDataExportOutput", "Bundle", "BundleEntry", "BundleEntryRequest", "BundleEntryResponse", "BundleEntrySearch", "BundleLink", "CapabilityStatement", "CapabilityStatementDocument", "CapabilityStatementImplementation", "CapabilityStatementMessaging", "CapabilityStatementMessagingEndpoint", "CapabilityStatementMessagingSupportedMessage", "CapabilityStatementRest", "CapabilityStatementRestInteraction", "CapabilityStatementRestResource", "CapabilityStatementRestResourceInteraction", "CapabilityStatementRestResourceOperation", "CapabilityStatementRestResourceSearchParam", "CapabilityStatementRestSecurity", "CapabilityStatementSoftware", "CarePlan", "CarePlanActivity", "CarePlanActivityDetail", "CareTeam", "CareTeamParticipant", "CatalogEntry", "CatalogEntryRelatedEntry", "ChargeItem", "ChargeItemDefinition", "ChargeItemDefinitionApplicability", "ChargeItemDefinitionPropertyGroup", "ChargeItemDefinitionPropertyGroupPriceComponent", "ChargeItemPerformer", "Claim", "ClaimAccident", "ClaimCareTeam", "ClaimDiagnosis", "ClaimInsurance", "ClaimItem", "ClaimItemDetail", "ClaimItemDetailSubDetail", "ClaimPayee", "ClaimProcedure", "ClaimRelated", "ClaimResponse", "ClaimResponseAddItem", "ClaimResponseAddItemDetail", "ClaimResponseAddItemDetailSubDetail", "ClaimResponseError", "ClaimResponseInsurance", "ClaimResponseItem", "ClaimResponseItemAdjudication", "ClaimResponseItemDetail", "ClaimResponseItemDetailSubDetail", "ClaimResponsePayment", "ClaimResponseProcessNote", "ClaimResponseTotal", "ClaimSupportingInfo", "ClientApplication", "ClientApplicationSignInForm", "ClinicalImpression", "ClinicalImpressionFinding", "ClinicalImpressionInvestigation", "CodeSystem", "CodeSystemConcept", "CodeSystemConceptDesignation", "CodeSystemConceptProperty", "CodeSystemFilter", "CodeSystemProperty", "CodeableConcept", "Coding", "Communication", "CommunicationPayload", "CommunicationRequest", "CommunicationRequestPayload", "CompartmentDefinition", "CompartmentDefinitionResource", "Composition", "CompositionAttester", "CompositionEvent", "CompositionRelatesTo", "CompositionSection", "ConceptMap", "ConceptMapGroup", "ConceptMapGroupElement", "ConceptMapGroupElementTarget", "ConceptMapGroupElementTargetDependsOn", "ConceptMapGroupUnmapped", "Condition", "ConditionEvidence", "ConditionStage", "Consent", "ConsentPolicy", "ConsentProvision", "ConsentProvisionActor", "ConsentProvisionData", "ConsentVerification", "ContactDetail", "ContactPoint", "Contract", "ContractContentDefinition", "ContractFriendly", "ContractLegal", "ContractRule", "ContractSigner", "ContractTerm", "ContractTermAction", "ContractTermActionSubject", "ContractTermAsset", "ContractTermAssetContext", "ContractTermAssetValuedItem", "ContractTermOffer", "ContractTermOfferAnswer", "ContractTermOfferParty", "ContractTermSecurityLabel", "Contributor", "Count", "Coverage", "CoverageClass", "CoverageCostToBeneficiary", "CoverageCostToBeneficiaryException", "CoverageEligibilityRequest", "CoverageEligibilityRequestInsurance", "CoverageEligibilityRequestItem", "CoverageEligibilityRequestItemDiagnosis", "CoverageEligibilityRequestSupportingInfo", "CoverageEligibilityResponse", "CoverageEligibilityResponseError", "CoverageEligibilityResponseInsurance", "CoverageEligibilityResponseInsuranceItem", "CoverageEligibilityResponseInsuranceItemBenefit", "DataRequirement", "DataRequirementCodeFilter", "DataRequirementDateFilter", "DataRequirementSort", "DetectedIssue", "DetectedIssueEvidence", "DetectedIssueMitigation", "Device", "DeviceDefinition", "DeviceDefinitionCapability", "DeviceDefinitionClassification", "DeviceDefinitionDeviceName", "DeviceDefinitionMaterial", "DeviceDefinitionProperty", "DeviceDefinitionSpecialization", "DeviceDefinitionUdiDeviceIdentifier", "DeviceDeviceName", "DeviceMetric", "DeviceMetricCalibration", "DeviceProperty", "DeviceRequest", "DeviceRequestParameter", "DeviceSpecialization", "DeviceUdiCarrier", "DeviceUseStatement", "DeviceVersion", "DiagnosticReport", "DiagnosticReportMedia", "Distance", "DocumentManifest", "DocumentManifestRelated", "DocumentReference", "DocumentReferenceContent", "DocumentReferenceContext", "DocumentReferenceRelatesTo", "DomainConfiguration", "Dosage", "DosageDoseAndRate", "Duration", "EffectEvidenceSynthesis", "EffectEvidenceSynthesisCertainty", "EffectEvidenceSynthesisCertaintyCertaintySubcomponent", "EffectEvidenceSynthesisEffectEstimate", "EffectEvidenceSynthesisEffectEstimatePrecisionEstimate", "EffectEvidenceSynthesisResultsByExposure", "EffectEvidenceSynthesisSampleSize", "Element", "ElementDefinition", "ElementDefinitionBase", "ElementDefinitionBinding", "ElementDefinitionConstraint", "ElementDefinitionExample", "ElementDefinitionMapping", "ElementDefinitionSlicing", "ElementDefinitionSlicingDiscriminator", "ElementDefinitionType", "Encounter", "EncounterClassHistory", "EncounterDiagnosis", "EncounterHospitalization", "EncounterLocation", "EncounterParticipant", "EncounterStatusHistory", "Endpoint", "EnrollmentRequest", "EnrollmentResponse", "EpisodeOfCare", "EpisodeOfCareDiagnosis", "EpisodeOfCareStatusHistory", "EventDefinition", "Evidence", "EvidenceVariable", "EvidenceVariableCharacteristic", "EvidenceVariableCharacteristicDefinitionByCombination", "EvidenceVariableCharacteristicDefinitionByTypeAndValue", "EvidenceVariableCharacteristicTimeFromEvent", "ExampleScenario", "ExampleScenarioActor", "ExampleScenarioInstance", "ExampleScenarioInstanceContainedInstance", "ExampleScenarioInstanceVersion", "ExampleScenarioProcess", "ExampleScenarioProcessStep", "ExampleScenarioProcessStepAlternative", "ExampleScenarioProcessStepOperation", "ExplanationOfBenefit", "ExplanationOfBenefitAccident", "ExplanationOfBenefitAddItem", "ExplanationOfBenefitAddItemDetail", "ExplanationOfBenefitAddItemDetailSubDetail", "ExplanationOfBenefitBenefitBalance", "ExplanationOfBenefitBenefitBalanceFinancial", "ExplanationOfBenefitCareTeam", "ExplanationOfBenefitDiagnosis", "ExplanationOfBenefitInsurance", "ExplanationOfBenefitItem", "ExplanationOfBenefitItemAdjudication", "ExplanationOfBenefitItemDetail", "ExplanationOfBenefitItemDetailSubDetail", "ExplanationOfBenefitPayee", "ExplanationOfBenefitPayment", "ExplanationOfBenefitProcedure", "ExplanationOfBenefitProcessNote", "ExplanationOfBenefitRelated", "ExplanationOfBenefitSupportingInfo", "ExplanationOfBenefitTotal", "Expression", "Extension", "FamilyMemberHistory", "FamilyMemberHistoryCondition", "Flag", "Goal", "GoalTarget", "GraphDefinition", "GraphDefinitionLink", "GraphDefinitionLinkTarget", "GraphDefinitionLinkTargetCompartment", "Group", "GroupCharacteristic", "GroupMember", "GuidanceResponse", "HealthcareService", "HealthcareServiceAvailableTime", "HealthcareServiceEligibility", "HealthcareServiceNotAvailable", "HumanName", "Identifier", "IdentityProvider", "ImagingStudy", "ImagingStudySeries", "ImagingStudySeriesInstance", "ImagingStudySeriesPerformer", "Immunization", "ImmunizationEducation", "ImmunizationEvaluation", "ImmunizationPerformer", "ImmunizationProtocolApplied", "ImmunizationReaction", "ImmunizationRecommendation", "ImmunizationRecommendationRecommendation", "ImmunizationRecommendationRecommendationDateCriterion", "ImplementationGuide", "ImplementationGuideDefinition", "ImplementationGuideDefinitionGrouping", "ImplementationGuideDefinitionPage", "ImplementationGuideDefinitionParameter", "ImplementationGuideDefinitionResource", "ImplementationGuideDefinitionTemplate", "ImplementationGuideDependsOn", "ImplementationGuideGlobal", "ImplementationGuideManifest", "ImplementationGuideManifestPage", "ImplementationGuideManifestResource", "InsurancePlan", "InsurancePlanContact", "InsurancePlanCoverage", "InsurancePlanCoverageBenefit", "InsurancePlanCoverageBenefitLimit", "InsurancePlanPlan", "InsurancePlanPlanGeneralCost", "InsurancePlanPlanSpecificCost", "InsurancePlanPlanSpecificCostBenefit", "InsurancePlanPlanSpecificCostBenefitCost", "Invoice", "InvoiceLineItem", "InvoiceLineItemPriceComponent", "InvoiceParticipant", "JsonWebKey", "Library", "Linkage", "LinkageItem", "List", "ListEntry", "Location", "LocationHoursOfOperation", "LocationPosition", "Login", "MarketingStatus", "Measure", "MeasureGroup", "MeasureGroupPopulation", "MeasureGroupStratifier", "MeasureGroupStratifierComponent", "MeasureReport", "MeasureReportGroup", "MeasureReportGroupPopulation", "MeasureReportGroupStratifier", "MeasureReportGroupStratifierStratum", "MeasureReportGroupStratifierStratumComponent", "MeasureReportGroupStratifierStratumPopulation", "MeasureSupplementalData", "Media", "Medication", "MedicationAdministration", "MedicationAdministrationDosage", "MedicationAdministrationPerformer", "MedicationBatch", "MedicationDispense", "MedicationDispensePerformer", "MedicationDispenseSubstitution", "MedicationIngredient", "MedicationKnowledge", "MedicationKnowledgeAdministrationGuidelines", "MedicationKnowledgeAdministrationGuidelinesDosage", "MedicationKnowledgeAdministrationGuidelinesPatientCharacteristics", "MedicationKnowledgeCost", "MedicationKnowledgeDrugCharacteristic", "MedicationKnowledgeIngredient", "MedicationKnowledgeKinetics", "MedicationKnowledgeMedicineClassification", "MedicationKnowledgeMonitoringProgram", "MedicationKnowledgeMonograph", "MedicationKnowledgePackaging", "MedicationKnowledgeRegulatory", "MedicationKnowledgeRegulatoryMaxDispense", "MedicationKnowledgeRegulatorySchedule", "MedicationKnowledgeRegulatorySubstitution", "MedicationKnowledgeRelatedMedicationKnowledge", "MedicationRequest", "MedicationRequestDispenseRequest", "MedicationRequestDispenseRequestInitialFill", "MedicationRequestSubstitution", "MedicationStatement", "MedicinalProduct", "MedicinalProductAuthorization", "MedicinalProductAuthorizationJurisdictionalAuthorization", "MedicinalProductAuthorizationProcedure", "MedicinalProductContraindication", "MedicinalProductContraindicationOtherTherapy", "MedicinalProductIndication", "MedicinalProductIndicationOtherTherapy", "MedicinalProductIngredient", "MedicinalProductIngredientSpecifiedSubstance", "MedicinalProductIngredientSpecifiedSubstanceStrength", "MedicinalProductIngredientSpecifiedSubstanceStrengthReferenceStrength", "MedicinalProductIngredientSubstance", "MedicinalProductInteraction", "MedicinalProductInteractionInteractant", "MedicinalProductManufactured", "MedicinalProductManufacturingBusinessOperation", "MedicinalProductName", "MedicinalProductNameCountryLanguage", "MedicinalProductNameNamePart", "MedicinalProductPackaged", "MedicinalProductPackagedBatchIdentifier", "MedicinalProductPackagedPackageItem", "MedicinalProductPharmaceutical", "MedicinalProductPharmaceuticalCharacteristics", "MedicinalProductPharmaceuticalRouteOfAdministration", "MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpecies", "MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpeciesWithdrawalPeriod", "MedicinalProductSpecialDesignation", "MedicinalProductUndesirableEffect", "MessageDefinition", "MessageDefinitionAllowedResponse", "MessageDefinitionFocus", "MessageHeader", "MessageHeaderDestination", "MessageHeaderResponse", "MessageHeaderSource", "Meta", "MetadataResource", "MolecularSequence", "MolecularSequenceQuality", "MolecularSequenceQualityRoc", "MolecularSequenceReferenceSeq", "MolecularSequenceRepository", "MolecularSequenceStructureVariant", "MolecularSequenceStructureVariantInner", "MolecularSequenceStructureVariantOuter", "MolecularSequenceVariant", "Money", "MoneyQuantity", "NamingSystem", "NamingSystemUniqueId", "Narrative", "NutritionOrder", "NutritionOrderEnteralFormula", "NutritionOrderEnteralFormulaAdministration", "NutritionOrderOralDiet", "NutritionOrderOralDietNutrient", "NutritionOrderOralDietTexture", "NutritionOrderSupplement", "Observation", "ObservationComponent", "ObservationDefinition", "ObservationDefinitionQualifiedInterval", "ObservationDefinitionQuantitativeDetails", "ObservationReferenceRange", "OperationDefinition", "OperationDefinitionOverload", "OperationDefinitionParameter", "OperationDefinitionParameterBinding", "OperationDefinitionParameterReferencedFrom", "OperationOutcome", "OperationOutcomeIssue", "Organization", "OrganizationAffiliation", "OrganizationContact", "ParameterDefinition", "Parameters", "ParametersParameter", "PasswordChangeRequest", "Patient", "PatientCommunication", "PatientContact", "PatientLink", "PaymentNotice", "PaymentReconciliation", "PaymentReconciliationDetail", "PaymentReconciliationProcessNote", "Period", "Person", "PersonLink", "PlanDefinition", "PlanDefinitionAction", "PlanDefinitionActionCondition", "PlanDefinitionActionDynamicValue", "PlanDefinitionActionParticipant", "PlanDefinitionActionRelatedAction", "PlanDefinitionGoal", "PlanDefinitionGoalTarget", "Population", "Practitioner", "PractitionerQualification", "PractitionerRole", "PractitionerRoleAvailableTime", "PractitionerRoleNotAvailable", "Procedure", "ProcedureFocalDevice", "ProcedurePerformer", "ProdCharacteristic", "ProductShelfLife", "Project", "ProjectDefaultProfile", "ProjectLink", "ProjectMembership", "ProjectMembershipAccess", "ProjectMembershipAccessParameter", "ProjectSetting", "ProjectSite", "Provenance", "ProvenanceAgent", "ProvenanceEntity", "Quantity", "Questionnaire", "QuestionnaireItem", "QuestionnaireItemAnswerOption", "QuestionnaireItemEnableWhen", "QuestionnaireItemInitial", "QuestionnaireResponse", "QuestionnaireResponseItem", "QuestionnaireResponseItemAnswer", "Range", "Ratio", "Reference", "RelatedArtifact", "RelatedPerson", "RelatedPersonCommunication", "RequestGroup", "RequestGroupAction", "RequestGroupActionCondition", "RequestGroupActionRelatedAction", "ResearchDefinition", "ResearchElementDefinition", "ResearchElementDefinitionCharacteristic", "ResearchStudy", "ResearchStudyArm", "ResearchStudyAssociatedParty", "ResearchStudyComparisonGroup", "ResearchStudyLabel", "ResearchStudyObjective", "ResearchStudyOutcomeMeasure", "ResearchStudyProgressStatus", "ResearchStudyRecruitment", "ResearchSubject", "RiskAssessment", "RiskAssessmentPrediction", "RiskEvidenceSynthesis", "RiskEvidenceSynthesisCertainty", "RiskEvidenceSynthesisCertaintyCertaintySubcomponent", "RiskEvidenceSynthesisRiskEstimate", "RiskEvidenceSynthesisRiskEstimatePrecisionEstimate", "RiskEvidenceSynthesisSampleSize", "SampledData", "Schedule", "SearchParameter", "SearchParameterComponent", "ServiceRequest", "Signature", "SimpleQuantity", "Slot", "SmartAppLaunch", "Specimen", "SpecimenCollection", "SpecimenContainer", "SpecimenDefinition", "SpecimenDefinitionTypeTested", "SpecimenDefinitionTypeTestedContainer", "SpecimenDefinitionTypeTestedContainerAdditive", "SpecimenDefinitionTypeTestedHandling", "SpecimenProcessing", "StructureDefinition", "StructureDefinitionContext", "StructureDefinitionDifferential", "StructureDefinitionMapping", "StructureDefinitionSnapshot", "StructureMap", "StructureMapGroup", "StructureMapGroupInput", "StructureMapGroupRule", "StructureMapGroupRuleDependent", "StructureMapGroupRuleSource", "StructureMapGroupRuleTarget", "StructureMapGroupRuleTargetParameter", "StructureMapStructure", "Subscription", "SubscriptionChannel", "SubscriptionStatus", "SubscriptionStatusNotificationEvent", "Substance", "SubstanceAmount", "SubstanceAmountReferenceRange", "SubstanceIngredient", "SubstanceInstance", "SubstanceNucleicAcid", "SubstanceNucleicAcidSubunit", "SubstanceNucleicAcidSubunitLinkage", "SubstanceNucleicAcidSubunitSugar", "SubstancePolymer", "SubstancePolymerMonomerSet", "SubstancePolymerMonomerSetStartingMaterial", "SubstancePolymerRepeat", "SubstancePolymerRepeatRepeatUnit", "SubstancePolymerRepeatRepeatUnitDegreeOfPolymerisation", "SubstancePolymerRepeatRepeatUnitStructuralRepresentation", "SubstanceProtein", "SubstanceProteinSubunit", "SubstanceReferenceInformation", "SubstanceReferenceInformationClassification", "SubstanceReferenceInformationGene", "SubstanceReferenceInformationGeneElement", "SubstanceReferenceInformationTarget", "SubstanceSourceMaterial", "SubstanceSourceMaterialFractionDescription", "SubstanceSourceMaterialOrganism", "SubstanceSourceMaterialOrganismAuthor", "SubstanceSourceMaterialOrganismHybrid", "SubstanceSourceMaterialOrganismOrganismGeneral", "SubstanceSourceMaterialPartDescription", "SubstanceSpecification", "SubstanceSpecificationCode", "SubstanceSpecificationMoiety", "SubstanceSpecificationName", "SubstanceSpecificationNameOfficial", "SubstanceSpecificationProperty", "SubstanceSpecificationRelationship", "SubstanceSpecificationStructure", "SubstanceSpecificationStructureIsotope", "SubstanceSpecificationStructureIsotopeMolecularWeight", "SubstanceSpecificationStructureRepresentation", "SupplyDelivery", "SupplyDeliverySuppliedItem", "SupplyRequest", "SupplyRequestParameter", "Task", "TaskInput", "TaskOutput", "TaskRestriction", "TerminologyCapabilities", "TerminologyCapabilitiesClosure", "TerminologyCapabilitiesCodeSystem", "TerminologyCapabilitiesCodeSystemVersion", "TerminologyCapabilitiesCodeSystemVersionFilter", "TerminologyCapabilitiesExpansion", "TerminologyCapabilitiesExpansionParameter", "TerminologyCapabilitiesImplementation", "TerminologyCapabilitiesSoftware", "TerminologyCapabilitiesTranslation", "TerminologyCapabilitiesValidateCode", "TestReport", "TestReportParticipant", "TestReportSetup", "TestReportSetupAction", "TestReportSetupActionAssert", "TestReportSetupActionOperation", "TestReportTeardown", "TestReportTeardownAction", "TestReportTest", "TestReportTestAction", "TestScript", "TestScriptDestination", "TestScriptFixture", "TestScriptMetadata", "TestScriptMetadataCapability", "TestScriptMetadataLink", "TestScriptOrigin", "TestScriptSetup", "TestScriptSetupAction", "TestScriptSetupActionAssert", "TestScriptSetupActionOperation", "TestScriptSetupActionOperationRequestHeader", "TestScriptTeardown", "TestScriptTeardownAction", "TestScriptTest", "TestScriptTestAction", "TestScriptVariable", "Timing", "TimingRepeat", "TriggerDefinition", "UsageContext", "User", "UserConfiguration", "UserConfigurationMenu", "UserConfigurationMenuLink", "UserConfigurationOption", "UserConfigurationSearch", "UserSecurityRequest", "ValueSet", "ValueSetCompose", "ValueSetComposeInclude", "ValueSetComposeIncludeConcept", "ValueSetComposeIncludeConceptDesignation", "ValueSetComposeIncludeFilter", "ValueSetExpansion", "ValueSetExpansionContains", "ValueSetExpansionParameter", "VerificationResult", "VerificationResultAttestation", "VerificationResultPrimarySource", "VerificationResultValidator", "ViewDefinition", "ViewDefinitionConstant", "ViewDefinitionSelect", "ViewDefinitionSelectColumn", "ViewDefinitionSelectColumnTag", "ViewDefinitionWhere", "VisionPrescription", "VisionPrescriptionLensSpecification", "VisionPrescriptionLensSpecificationPrism"]

if TYPE_CHECKING:
    # Resource is a union of all FHIR resource types
    # Import all resources for type checking
    from pymedplum.fhir.accesspolicy import AccessPolicy, AccessPolicyIpAccessRule, AccessPolicyResource
    from pymedplum.fhir.account import Account, AccountCoverage, AccountGuarantor
    from pymedplum.fhir.activitydefinition import ActivityDefinition, ActivityDefinitionDynamicValue, ActivityDefinitionParticipant
    from pymedplum.fhir.address import Address
    from pymedplum.fhir.adverseevent import AdverseEvent, AdverseEventSuspectEntity, AdverseEventSuspectEntityCausality
    from pymedplum.fhir.age import Age
    from pymedplum.fhir.agent import Agent, AgentChannel, AgentSetting
    from pymedplum.fhir.allergyintolerance import AllergyIntolerance, AllergyIntoleranceReaction
    from pymedplum.fhir.annotation import Annotation
    from pymedplum.fhir.appointment import Appointment, AppointmentParticipant
    from pymedplum.fhir.appointmentresponse import AppointmentResponse
    from pymedplum.fhir.asyncjob import AsyncJob
    from pymedplum.fhir.attachment import Attachment
    from pymedplum.fhir.auditevent import AuditEvent, AuditEventAgent, AuditEventAgentNetwork, AuditEventEntity, AuditEventEntityDetail, AuditEventSource
    from pymedplum.fhir.backboneelement import BackboneElement
    from pymedplum.fhir.basic import Basic
    from pymedplum.fhir.binary import Binary
    from pymedplum.fhir.biologicallyderivedproduct import BiologicallyDerivedProduct, BiologicallyDerivedProductCollection, BiologicallyDerivedProductManipulation, BiologicallyDerivedProductProcessing, BiologicallyDerivedProductStorage
    from pymedplum.fhir.bodystructure import BodyStructure
    from pymedplum.fhir.bot import Bot
    from pymedplum.fhir.bulkdataexport import BulkDataExport, BulkDataExportDeleted, BulkDataExportError, BulkDataExportOutput
    from pymedplum.fhir.bundle import Bundle, BundleEntry, BundleEntryRequest, BundleEntryResponse, BundleEntrySearch, BundleLink
    from pymedplum.fhir.capabilitystatement import CapabilityStatement, CapabilityStatementDocument, CapabilityStatementImplementation, CapabilityStatementMessaging, CapabilityStatementMessagingEndpoint, CapabilityStatementMessagingSupportedMessage, CapabilityStatementRest, CapabilityStatementRestInteraction, CapabilityStatementRestResource, CapabilityStatementRestResourceInteraction, CapabilityStatementRestResourceOperation, CapabilityStatementRestResourceSearchParam, CapabilityStatementRestSecurity, CapabilityStatementSoftware
    from pymedplum.fhir.careplan import CarePlan, CarePlanActivity, CarePlanActivityDetail
    from pymedplum.fhir.careteam import CareTeam, CareTeamParticipant
    from pymedplum.fhir.catalogentry import CatalogEntry, CatalogEntryRelatedEntry
    from pymedplum.fhir.chargeitem import ChargeItem, ChargeItemPerformer
    from pymedplum.fhir.chargeitemdefinition import ChargeItemDefinition, ChargeItemDefinitionApplicability, ChargeItemDefinitionPropertyGroup, ChargeItemDefinitionPropertyGroupPriceComponent
    from pymedplum.fhir.claim import Claim, ClaimAccident, ClaimCareTeam, ClaimDiagnosis, ClaimInsurance, ClaimItem, ClaimItemDetail, ClaimItemDetailSubDetail, ClaimPayee, ClaimProcedure, ClaimRelated, ClaimSupportingInfo
    from pymedplum.fhir.claimresponse import ClaimResponse, ClaimResponseAddItem, ClaimResponseAddItemDetail, ClaimResponseAddItemDetailSubDetail, ClaimResponseError, ClaimResponseInsurance, ClaimResponseItem, ClaimResponseItemAdjudication, ClaimResponseItemDetail, ClaimResponseItemDetailSubDetail, ClaimResponsePayment, ClaimResponseProcessNote, ClaimResponseTotal
    from pymedplum.fhir.clientapplication import ClientApplication, ClientApplicationSignInForm
    from pymedplum.fhir.clinicalimpression import ClinicalImpression, ClinicalImpressionFinding, ClinicalImpressionInvestigation
    from pymedplum.fhir.codeableconcept import CodeableConcept
    from pymedplum.fhir.codesystem import CodeSystem, CodeSystemConcept, CodeSystemConceptDesignation, CodeSystemConceptProperty, CodeSystemFilter, CodeSystemProperty
    from pymedplum.fhir.coding import Coding
    from pymedplum.fhir.communication import Communication, CommunicationPayload
    from pymedplum.fhir.communicationrequest import CommunicationRequest, CommunicationRequestPayload
    from pymedplum.fhir.compartmentdefinition import CompartmentDefinition, CompartmentDefinitionResource
    from pymedplum.fhir.composition import Composition, CompositionAttester, CompositionEvent, CompositionRelatesTo, CompositionSection
    from pymedplum.fhir.conceptmap import ConceptMap, ConceptMapGroup, ConceptMapGroupElement, ConceptMapGroupElementTarget, ConceptMapGroupElementTargetDependsOn, ConceptMapGroupUnmapped
    from pymedplum.fhir.condition import Condition, ConditionEvidence, ConditionStage
    from pymedplum.fhir.consent import Consent, ConsentPolicy, ConsentProvision, ConsentProvisionActor, ConsentProvisionData, ConsentVerification
    from pymedplum.fhir.contactdetail import ContactDetail
    from pymedplum.fhir.contactpoint import ContactPoint
    from pymedplum.fhir.contract import Contract, ContractContentDefinition, ContractFriendly, ContractLegal, ContractRule, ContractSigner, ContractTerm, ContractTermAction, ContractTermActionSubject, ContractTermAsset, ContractTermAssetContext, ContractTermAssetValuedItem, ContractTermOffer, ContractTermOfferAnswer, ContractTermOfferParty, ContractTermSecurityLabel
    from pymedplum.fhir.contributor import Contributor
    from pymedplum.fhir.count import Count
    from pymedplum.fhir.coverage import Coverage, CoverageClass, CoverageCostToBeneficiary, CoverageCostToBeneficiaryException
    from pymedplum.fhir.coverageeligibilityrequest import CoverageEligibilityRequest, CoverageEligibilityRequestInsurance, CoverageEligibilityRequestItem, CoverageEligibilityRequestItemDiagnosis, CoverageEligibilityRequestSupportingInfo
    from pymedplum.fhir.coverageeligibilityresponse import CoverageEligibilityResponse, CoverageEligibilityResponseError, CoverageEligibilityResponseInsurance, CoverageEligibilityResponseInsuranceItem, CoverageEligibilityResponseInsuranceItemBenefit
    from pymedplum.fhir.datarequirement import DataRequirement, DataRequirementCodeFilter, DataRequirementDateFilter, DataRequirementSort
    from pymedplum.fhir.detectedissue import DetectedIssue, DetectedIssueEvidence, DetectedIssueMitigation
    from pymedplum.fhir.device import Device, DeviceDeviceName, DeviceProperty, DeviceSpecialization, DeviceUdiCarrier, DeviceVersion
    from pymedplum.fhir.devicedefinition import DeviceDefinition, DeviceDefinitionCapability, DeviceDefinitionClassification, DeviceDefinitionDeviceName, DeviceDefinitionMaterial, DeviceDefinitionProperty, DeviceDefinitionSpecialization, DeviceDefinitionUdiDeviceIdentifier
    from pymedplum.fhir.devicemetric import DeviceMetric, DeviceMetricCalibration
    from pymedplum.fhir.devicerequest import DeviceRequest, DeviceRequestParameter
    from pymedplum.fhir.deviceusestatement import DeviceUseStatement
    from pymedplum.fhir.diagnosticreport import DiagnosticReport, DiagnosticReportMedia
    from pymedplum.fhir.distance import Distance
    from pymedplum.fhir.documentmanifest import DocumentManifest, DocumentManifestRelated
    from pymedplum.fhir.documentreference import DocumentReference, DocumentReferenceContent, DocumentReferenceContext, DocumentReferenceRelatesTo
    from pymedplum.fhir.domainconfiguration import DomainConfiguration
    from pymedplum.fhir.dosage import Dosage, DosageDoseAndRate
    from pymedplum.fhir.duration import Duration
    from pymedplum.fhir.effectevidencesynthesis import EffectEvidenceSynthesis, EffectEvidenceSynthesisCertainty, EffectEvidenceSynthesisCertaintyCertaintySubcomponent, EffectEvidenceSynthesisEffectEstimate, EffectEvidenceSynthesisEffectEstimatePrecisionEstimate, EffectEvidenceSynthesisResultsByExposure, EffectEvidenceSynthesisSampleSize
    from pymedplum.fhir.element import Element
    from pymedplum.fhir.elementdefinition import ElementDefinition, ElementDefinitionBase, ElementDefinitionBinding, ElementDefinitionConstraint, ElementDefinitionExample, ElementDefinitionMapping, ElementDefinitionSlicing, ElementDefinitionSlicingDiscriminator, ElementDefinitionType
    from pymedplum.fhir.encounter import Encounter, EncounterClassHistory, EncounterDiagnosis, EncounterHospitalization, EncounterLocation, EncounterParticipant, EncounterStatusHistory
    from pymedplum.fhir.endpoint import Endpoint
    from pymedplum.fhir.enrollmentrequest import EnrollmentRequest
    from pymedplum.fhir.enrollmentresponse import EnrollmentResponse
    from pymedplum.fhir.episodeofcare import EpisodeOfCare, EpisodeOfCareDiagnosis, EpisodeOfCareStatusHistory
    from pymedplum.fhir.eventdefinition import EventDefinition
    from pymedplum.fhir.evidence import Evidence
    from pymedplum.fhir.evidencevariable import EvidenceVariable, EvidenceVariableCharacteristic, EvidenceVariableCharacteristicDefinitionByCombination, EvidenceVariableCharacteristicDefinitionByTypeAndValue, EvidenceVariableCharacteristicTimeFromEvent
    from pymedplum.fhir.examplescenario import ExampleScenario, ExampleScenarioActor, ExampleScenarioInstance, ExampleScenarioInstanceContainedInstance, ExampleScenarioInstanceVersion, ExampleScenarioProcess, ExampleScenarioProcessStep, ExampleScenarioProcessStepAlternative, ExampleScenarioProcessStepOperation
    from pymedplum.fhir.explanationofbenefit import ExplanationOfBenefit, ExplanationOfBenefitAccident, ExplanationOfBenefitAddItem, ExplanationOfBenefitAddItemDetail, ExplanationOfBenefitAddItemDetailSubDetail, ExplanationOfBenefitBenefitBalance, ExplanationOfBenefitBenefitBalanceFinancial, ExplanationOfBenefitCareTeam, ExplanationOfBenefitDiagnosis, ExplanationOfBenefitInsurance, ExplanationOfBenefitItem, ExplanationOfBenefitItemAdjudication, ExplanationOfBenefitItemDetail, ExplanationOfBenefitItemDetailSubDetail, ExplanationOfBenefitPayee, ExplanationOfBenefitPayment, ExplanationOfBenefitProcedure, ExplanationOfBenefitProcessNote, ExplanationOfBenefitRelated, ExplanationOfBenefitSupportingInfo, ExplanationOfBenefitTotal
    from pymedplum.fhir.expression import Expression
    from pymedplum.fhir.extension import Extension
    from pymedplum.fhir.familymemberhistory import FamilyMemberHistory, FamilyMemberHistoryCondition
    from pymedplum.fhir.flag import Flag
    from pymedplum.fhir.goal import Goal, GoalTarget
    from pymedplum.fhir.graphdefinition import GraphDefinition, GraphDefinitionLink, GraphDefinitionLinkTarget, GraphDefinitionLinkTargetCompartment
    from pymedplum.fhir.group import Group, GroupCharacteristic, GroupMember
    from pymedplum.fhir.guidanceresponse import GuidanceResponse
    from pymedplum.fhir.healthcareservice import HealthcareService, HealthcareServiceAvailableTime, HealthcareServiceEligibility, HealthcareServiceNotAvailable
    from pymedplum.fhir.humanname import HumanName
    from pymedplum.fhir.identifier import Identifier
    from pymedplum.fhir.identityprovider import IdentityProvider
    from pymedplum.fhir.imagingstudy import ImagingStudy, ImagingStudySeries, ImagingStudySeriesInstance, ImagingStudySeriesPerformer
    from pymedplum.fhir.immunization import Immunization, ImmunizationEducation, ImmunizationPerformer, ImmunizationProtocolApplied, ImmunizationReaction
    from pymedplum.fhir.immunizationevaluation import ImmunizationEvaluation
    from pymedplum.fhir.immunizationrecommendation import ImmunizationRecommendation, ImmunizationRecommendationRecommendation, ImmunizationRecommendationRecommendationDateCriterion
    from pymedplum.fhir.implementationguide import ImplementationGuide, ImplementationGuideDefinition, ImplementationGuideDefinitionGrouping, ImplementationGuideDefinitionPage, ImplementationGuideDefinitionParameter, ImplementationGuideDefinitionResource, ImplementationGuideDefinitionTemplate, ImplementationGuideDependsOn, ImplementationGuideGlobal, ImplementationGuideManifest, ImplementationGuideManifestPage, ImplementationGuideManifestResource
    from pymedplum.fhir.insuranceplan import InsurancePlan, InsurancePlanContact, InsurancePlanCoverage, InsurancePlanCoverageBenefit, InsurancePlanCoverageBenefitLimit, InsurancePlanPlan, InsurancePlanPlanGeneralCost, InsurancePlanPlanSpecificCost, InsurancePlanPlanSpecificCostBenefit, InsurancePlanPlanSpecificCostBenefitCost
    from pymedplum.fhir.invoice import Invoice, InvoiceLineItem, InvoiceLineItemPriceComponent, InvoiceParticipant
    from pymedplum.fhir.jsonwebkey import JsonWebKey
    from pymedplum.fhir.library import Library
    from pymedplum.fhir.linkage import Linkage, LinkageItem
    from pymedplum.fhir.list import List, ListEntry
    from pymedplum.fhir.location import Location, LocationHoursOfOperation, LocationPosition
    from pymedplum.fhir.login import Login
    from pymedplum.fhir.marketingstatus import MarketingStatus
    from pymedplum.fhir.measure import Measure, MeasureGroup, MeasureGroupPopulation, MeasureGroupStratifier, MeasureGroupStratifierComponent, MeasureSupplementalData
    from pymedplum.fhir.measurereport import MeasureReport, MeasureReportGroup, MeasureReportGroupPopulation, MeasureReportGroupStratifier, MeasureReportGroupStratifierStratum, MeasureReportGroupStratifierStratumComponent, MeasureReportGroupStratifierStratumPopulation
    from pymedplum.fhir.media import Media
    from pymedplum.fhir.medication import Medication, MedicationBatch, MedicationIngredient
    from pymedplum.fhir.medicationadministration import MedicationAdministration, MedicationAdministrationDosage, MedicationAdministrationPerformer
    from pymedplum.fhir.medicationdispense import MedicationDispense, MedicationDispensePerformer, MedicationDispenseSubstitution
    from pymedplum.fhir.medicationknowledge import MedicationKnowledge, MedicationKnowledgeAdministrationGuidelines, MedicationKnowledgeAdministrationGuidelinesDosage, MedicationKnowledgeAdministrationGuidelinesPatientCharacteristics, MedicationKnowledgeCost, MedicationKnowledgeDrugCharacteristic, MedicationKnowledgeIngredient, MedicationKnowledgeKinetics, MedicationKnowledgeMedicineClassification, MedicationKnowledgeMonitoringProgram, MedicationKnowledgeMonograph, MedicationKnowledgePackaging, MedicationKnowledgeRegulatory, MedicationKnowledgeRegulatoryMaxDispense, MedicationKnowledgeRegulatorySchedule, MedicationKnowledgeRegulatorySubstitution, MedicationKnowledgeRelatedMedicationKnowledge
    from pymedplum.fhir.medicationrequest import MedicationRequest, MedicationRequestDispenseRequest, MedicationRequestDispenseRequestInitialFill, MedicationRequestSubstitution
    from pymedplum.fhir.medicationstatement import MedicationStatement
    from pymedplum.fhir.medicinalproduct import MedicinalProduct, MedicinalProductManufacturingBusinessOperation, MedicinalProductName, MedicinalProductNameCountryLanguage, MedicinalProductNameNamePart, MedicinalProductSpecialDesignation
    from pymedplum.fhir.medicinalproductauthorization import MedicinalProductAuthorization, MedicinalProductAuthorizationJurisdictionalAuthorization, MedicinalProductAuthorizationProcedure
    from pymedplum.fhir.medicinalproductcontraindication import MedicinalProductContraindication, MedicinalProductContraindicationOtherTherapy
    from pymedplum.fhir.medicinalproductindication import MedicinalProductIndication, MedicinalProductIndicationOtherTherapy
    from pymedplum.fhir.medicinalproductingredient import MedicinalProductIngredient, MedicinalProductIngredientSpecifiedSubstance, MedicinalProductIngredientSpecifiedSubstanceStrength, MedicinalProductIngredientSpecifiedSubstanceStrengthReferenceStrength, MedicinalProductIngredientSubstance
    from pymedplum.fhir.medicinalproductinteraction import MedicinalProductInteraction, MedicinalProductInteractionInteractant
    from pymedplum.fhir.medicinalproductmanufactured import MedicinalProductManufactured
    from pymedplum.fhir.medicinalproductpackaged import MedicinalProductPackaged, MedicinalProductPackagedBatchIdentifier, MedicinalProductPackagedPackageItem
    from pymedplum.fhir.medicinalproductpharmaceutical import MedicinalProductPharmaceutical, MedicinalProductPharmaceuticalCharacteristics, MedicinalProductPharmaceuticalRouteOfAdministration, MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpecies, MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpeciesWithdrawalPeriod
    from pymedplum.fhir.medicinalproductundesirableeffect import MedicinalProductUndesirableEffect
    from pymedplum.fhir.messagedefinition import MessageDefinition, MessageDefinitionAllowedResponse, MessageDefinitionFocus
    from pymedplum.fhir.messageheader import MessageHeader, MessageHeaderDestination, MessageHeaderResponse, MessageHeaderSource
    from pymedplum.fhir.meta import Meta
    from pymedplum.fhir.metadataresource import MetadataResource
    from pymedplum.fhir.molecularsequence import MolecularSequence, MolecularSequenceQuality, MolecularSequenceQualityRoc, MolecularSequenceReferenceSeq, MolecularSequenceRepository, MolecularSequenceStructureVariant, MolecularSequenceStructureVariantInner, MolecularSequenceStructureVariantOuter, MolecularSequenceVariant
    from pymedplum.fhir.money import Money
    from pymedplum.fhir.moneyquantity import MoneyQuantity
    from pymedplum.fhir.namingsystem import NamingSystem, NamingSystemUniqueId
    from pymedplum.fhir.narrative import Narrative
    from pymedplum.fhir.nutritionorder import NutritionOrder, NutritionOrderEnteralFormula, NutritionOrderEnteralFormulaAdministration, NutritionOrderOralDiet, NutritionOrderOralDietNutrient, NutritionOrderOralDietTexture, NutritionOrderSupplement
    from pymedplum.fhir.observation import Observation, ObservationComponent, ObservationReferenceRange
    from pymedplum.fhir.observationdefinition import ObservationDefinition, ObservationDefinitionQualifiedInterval, ObservationDefinitionQuantitativeDetails
    from pymedplum.fhir.operationdefinition import OperationDefinition, OperationDefinitionOverload, OperationDefinitionParameter, OperationDefinitionParameterBinding, OperationDefinitionParameterReferencedFrom
    from pymedplum.fhir.operationoutcome import OperationOutcome, OperationOutcomeIssue
    from pymedplum.fhir.organization import Organization, OrganizationContact
    from pymedplum.fhir.organizationaffiliation import OrganizationAffiliation
    from pymedplum.fhir.parameterdefinition import ParameterDefinition
    from pymedplum.fhir.parameters import Parameters, ParametersParameter
    from pymedplum.fhir.passwordchangerequest import PasswordChangeRequest
    from pymedplum.fhir.patient import Patient, PatientCommunication, PatientContact, PatientLink
    from pymedplum.fhir.paymentnotice import PaymentNotice
    from pymedplum.fhir.paymentreconciliation import PaymentReconciliation, PaymentReconciliationDetail, PaymentReconciliationProcessNote
    from pymedplum.fhir.period import Period
    from pymedplum.fhir.person import Person, PersonLink
    from pymedplum.fhir.plandefinition import PlanDefinition, PlanDefinitionAction, PlanDefinitionActionCondition, PlanDefinitionActionDynamicValue, PlanDefinitionActionParticipant, PlanDefinitionActionRelatedAction, PlanDefinitionGoal, PlanDefinitionGoalTarget
    from pymedplum.fhir.population import Population
    from pymedplum.fhir.practitioner import Practitioner, PractitionerQualification
    from pymedplum.fhir.practitionerrole import PractitionerRole, PractitionerRoleAvailableTime, PractitionerRoleNotAvailable
    from pymedplum.fhir.procedure import Procedure, ProcedureFocalDevice, ProcedurePerformer
    from pymedplum.fhir.prodcharacteristic import ProdCharacteristic
    from pymedplum.fhir.productshelflife import ProductShelfLife
    from pymedplum.fhir.project import Project, ProjectDefaultProfile, ProjectLink, ProjectSetting, ProjectSite
    from pymedplum.fhir.projectmembership import ProjectMembership, ProjectMembershipAccess, ProjectMembershipAccessParameter
    from pymedplum.fhir.provenance import Provenance, ProvenanceAgent, ProvenanceEntity
    from pymedplum.fhir.quantity import Quantity
    from pymedplum.fhir.questionnaire import Questionnaire, QuestionnaireItem, QuestionnaireItemAnswerOption, QuestionnaireItemEnableWhen, QuestionnaireItemInitial
    from pymedplum.fhir.questionnaireresponse import QuestionnaireResponse, QuestionnaireResponseItem, QuestionnaireResponseItemAnswer
    from pymedplum.fhir.range import Range
    from pymedplum.fhir.ratio import Ratio
    from pymedplum.fhir.reference import Reference
    from pymedplum.fhir.relatedartifact import RelatedArtifact
    from pymedplum.fhir.relatedperson import RelatedPerson, RelatedPersonCommunication
    from pymedplum.fhir.requestgroup import RequestGroup, RequestGroupAction, RequestGroupActionCondition, RequestGroupActionRelatedAction
    from pymedplum.fhir.researchdefinition import ResearchDefinition
    from pymedplum.fhir.researchelementdefinition import ResearchElementDefinition, ResearchElementDefinitionCharacteristic
    from pymedplum.fhir.researchstudy import ResearchStudy, ResearchStudyArm, ResearchStudyAssociatedParty, ResearchStudyComparisonGroup, ResearchStudyLabel, ResearchStudyObjective, ResearchStudyOutcomeMeasure, ResearchStudyProgressStatus, ResearchStudyRecruitment
    from pymedplum.fhir.researchsubject import ResearchSubject
    from pymedplum.fhir.riskassessment import RiskAssessment, RiskAssessmentPrediction
    from pymedplum.fhir.riskevidencesynthesis import RiskEvidenceSynthesis, RiskEvidenceSynthesisCertainty, RiskEvidenceSynthesisCertaintyCertaintySubcomponent, RiskEvidenceSynthesisRiskEstimate, RiskEvidenceSynthesisRiskEstimatePrecisionEstimate, RiskEvidenceSynthesisSampleSize
    from pymedplum.fhir.sampleddata import SampledData
    from pymedplum.fhir.schedule import Schedule
    from pymedplum.fhir.searchparameter import SearchParameter, SearchParameterComponent
    from pymedplum.fhir.servicerequest import ServiceRequest
    from pymedplum.fhir.signature import Signature
    from pymedplum.fhir.simplequantity import SimpleQuantity
    from pymedplum.fhir.slot import Slot
    from pymedplum.fhir.smartapplaunch import SmartAppLaunch
    from pymedplum.fhir.specimen import Specimen, SpecimenCollection, SpecimenContainer, SpecimenProcessing
    from pymedplum.fhir.specimendefinition import SpecimenDefinition, SpecimenDefinitionTypeTested, SpecimenDefinitionTypeTestedContainer, SpecimenDefinitionTypeTestedContainerAdditive, SpecimenDefinitionTypeTestedHandling
    from pymedplum.fhir.structuredefinition import StructureDefinition, StructureDefinitionContext, StructureDefinitionDifferential, StructureDefinitionMapping, StructureDefinitionSnapshot
    from pymedplum.fhir.structuremap import StructureMap, StructureMapGroup, StructureMapGroupInput, StructureMapGroupRule, StructureMapGroupRuleDependent, StructureMapGroupRuleSource, StructureMapGroupRuleTarget, StructureMapGroupRuleTargetParameter, StructureMapStructure
    from pymedplum.fhir.subscription import Subscription, SubscriptionChannel
    from pymedplum.fhir.subscriptionstatus import SubscriptionStatus, SubscriptionStatusNotificationEvent
    from pymedplum.fhir.substance import Substance, SubstanceIngredient, SubstanceInstance
    from pymedplum.fhir.substanceamount import SubstanceAmount, SubstanceAmountReferenceRange
    from pymedplum.fhir.substancenucleicacid import SubstanceNucleicAcid, SubstanceNucleicAcidSubunit, SubstanceNucleicAcidSubunitLinkage, SubstanceNucleicAcidSubunitSugar
    from pymedplum.fhir.substancepolymer import SubstancePolymer, SubstancePolymerMonomerSet, SubstancePolymerMonomerSetStartingMaterial, SubstancePolymerRepeat, SubstancePolymerRepeatRepeatUnit, SubstancePolymerRepeatRepeatUnitDegreeOfPolymerisation, SubstancePolymerRepeatRepeatUnitStructuralRepresentation
    from pymedplum.fhir.substanceprotein import SubstanceProtein, SubstanceProteinSubunit
    from pymedplum.fhir.substancereferenceinformation import SubstanceReferenceInformation, SubstanceReferenceInformationClassification, SubstanceReferenceInformationGene, SubstanceReferenceInformationGeneElement, SubstanceReferenceInformationTarget
    from pymedplum.fhir.substancesourcematerial import SubstanceSourceMaterial, SubstanceSourceMaterialFractionDescription, SubstanceSourceMaterialOrganism, SubstanceSourceMaterialOrganismAuthor, SubstanceSourceMaterialOrganismHybrid, SubstanceSourceMaterialOrganismOrganismGeneral, SubstanceSourceMaterialPartDescription
    from pymedplum.fhir.substancespecification import SubstanceSpecification, SubstanceSpecificationCode, SubstanceSpecificationMoiety, SubstanceSpecificationName, SubstanceSpecificationNameOfficial, SubstanceSpecificationProperty, SubstanceSpecificationRelationship, SubstanceSpecificationStructure, SubstanceSpecificationStructureIsotope, SubstanceSpecificationStructureIsotopeMolecularWeight, SubstanceSpecificationStructureRepresentation
    from pymedplum.fhir.supplydelivery import SupplyDelivery, SupplyDeliverySuppliedItem
    from pymedplum.fhir.supplyrequest import SupplyRequest, SupplyRequestParameter
    from pymedplum.fhir.task import Task, TaskInput, TaskOutput, TaskRestriction
    from pymedplum.fhir.terminologycapabilities import TerminologyCapabilities, TerminologyCapabilitiesClosure, TerminologyCapabilitiesCodeSystem, TerminologyCapabilitiesCodeSystemVersion, TerminologyCapabilitiesCodeSystemVersionFilter, TerminologyCapabilitiesExpansion, TerminologyCapabilitiesExpansionParameter, TerminologyCapabilitiesImplementation, TerminologyCapabilitiesSoftware, TerminologyCapabilitiesTranslation, TerminologyCapabilitiesValidateCode
    from pymedplum.fhir.testreport import TestReport, TestReportParticipant, TestReportSetup, TestReportSetupAction, TestReportSetupActionAssert, TestReportSetupActionOperation, TestReportTeardown, TestReportTeardownAction, TestReportTest, TestReportTestAction
    from pymedplum.fhir.testscript import TestScript, TestScriptDestination, TestScriptFixture, TestScriptMetadata, TestScriptMetadataCapability, TestScriptMetadataLink, TestScriptOrigin, TestScriptSetup, TestScriptSetupAction, TestScriptSetupActionAssert, TestScriptSetupActionOperation, TestScriptSetupActionOperationRequestHeader, TestScriptTeardown, TestScriptTeardownAction, TestScriptTest, TestScriptTestAction, TestScriptVariable
    from pymedplum.fhir.timing import Timing, TimingRepeat
    from pymedplum.fhir.triggerdefinition import TriggerDefinition
    from pymedplum.fhir.usagecontext import UsageContext
    from pymedplum.fhir.user import User
    from pymedplum.fhir.userconfiguration import UserConfiguration, UserConfigurationMenu, UserConfigurationMenuLink, UserConfigurationOption, UserConfigurationSearch
    from pymedplum.fhir.usersecurityrequest import UserSecurityRequest
    from pymedplum.fhir.valueset import ValueSet, ValueSetCompose, ValueSetComposeInclude, ValueSetComposeIncludeConcept, ValueSetComposeIncludeConceptDesignation, ValueSetComposeIncludeFilter, ValueSetExpansion, ValueSetExpansionContains, ValueSetExpansionParameter
    from pymedplum.fhir.verificationresult import VerificationResult, VerificationResultAttestation, VerificationResultPrimarySource, VerificationResultValidator
    from pymedplum.fhir.viewdefinition import ViewDefinition, ViewDefinitionConstant, ViewDefinitionSelect, ViewDefinitionSelectColumn, ViewDefinitionSelectColumnTag, ViewDefinitionWhere
    from pymedplum.fhir.visionprescription import VisionPrescription, VisionPrescriptionLensSpecification, VisionPrescriptionLensSpecificationPrism

    Resource = AccessPolicy | AccessPolicyIpAccessRule | AccessPolicyResource | Account | AccountCoverage | AccountGuarantor | ActivityDefinition | ActivityDefinitionDynamicValue | ActivityDefinitionParticipant | Address | AdverseEvent | AdverseEventSuspectEntity | AdverseEventSuspectEntityCausality | Age | Agent | AgentChannel | AgentSetting | AllergyIntolerance | AllergyIntoleranceReaction | Annotation | Appointment | AppointmentParticipant | AppointmentResponse | AsyncJob | Attachment | AuditEvent | AuditEventAgent | AuditEventAgentNetwork | AuditEventEntity | AuditEventEntityDetail | AuditEventSource | BackboneElement | Basic | Binary | BiologicallyDerivedProduct | BiologicallyDerivedProductCollection | BiologicallyDerivedProductManipulation | BiologicallyDerivedProductProcessing | BiologicallyDerivedProductStorage | BodyStructure | Bot | BulkDataExport | BulkDataExportDeleted | BulkDataExportError | BulkDataExportOutput | Bundle | BundleEntry | BundleEntryRequest | BundleEntryResponse | BundleEntrySearch | BundleLink | CapabilityStatement | CapabilityStatementDocument | CapabilityStatementImplementation | CapabilityStatementMessaging | CapabilityStatementMessagingEndpoint | CapabilityStatementMessagingSupportedMessage | CapabilityStatementRest | CapabilityStatementRestInteraction | CapabilityStatementRestResource | CapabilityStatementRestResourceInteraction | CapabilityStatementRestResourceOperation | CapabilityStatementRestResourceSearchParam | CapabilityStatementRestSecurity | CapabilityStatementSoftware | CarePlan | CarePlanActivity | CarePlanActivityDetail | CareTeam | CareTeamParticipant | CatalogEntry | CatalogEntryRelatedEntry | ChargeItem | ChargeItemDefinition | ChargeItemDefinitionApplicability | ChargeItemDefinitionPropertyGroup | ChargeItemDefinitionPropertyGroupPriceComponent | ChargeItemPerformer | Claim | ClaimAccident | ClaimCareTeam | ClaimDiagnosis | ClaimInsurance | ClaimItem | ClaimItemDetail | ClaimItemDetailSubDetail | ClaimPayee | ClaimProcedure | ClaimRelated | ClaimResponse | ClaimResponseAddItem | ClaimResponseAddItemDetail | ClaimResponseAddItemDetailSubDetail | ClaimResponseError | ClaimResponseInsurance | ClaimResponseItem | ClaimResponseItemAdjudication | ClaimResponseItemDetail | ClaimResponseItemDetailSubDetail | ClaimResponsePayment | ClaimResponseProcessNote | ClaimResponseTotal | ClaimSupportingInfo | ClientApplication | ClientApplicationSignInForm | ClinicalImpression | ClinicalImpressionFinding | ClinicalImpressionInvestigation | CodeSystem | CodeSystemConcept | CodeSystemConceptDesignation | CodeSystemConceptProperty | CodeSystemFilter | CodeSystemProperty | CodeableConcept | Coding | Communication | CommunicationPayload | CommunicationRequest | CommunicationRequestPayload | CompartmentDefinition | CompartmentDefinitionResource | Composition | CompositionAttester | CompositionEvent | CompositionRelatesTo | CompositionSection | ConceptMap | ConceptMapGroup | ConceptMapGroupElement | ConceptMapGroupElementTarget | ConceptMapGroupElementTargetDependsOn | ConceptMapGroupUnmapped | Condition | ConditionEvidence | ConditionStage | Consent | ConsentPolicy | ConsentProvision | ConsentProvisionActor | ConsentProvisionData | ConsentVerification | ContactDetail | ContactPoint | Contract | ContractContentDefinition | ContractFriendly | ContractLegal | ContractRule | ContractSigner | ContractTerm | ContractTermAction | ContractTermActionSubject | ContractTermAsset | ContractTermAssetContext | ContractTermAssetValuedItem | ContractTermOffer | ContractTermOfferAnswer | ContractTermOfferParty | ContractTermSecurityLabel | Contributor | Count | Coverage | CoverageClass | CoverageCostToBeneficiary | CoverageCostToBeneficiaryException | CoverageEligibilityRequest | CoverageEligibilityRequestInsurance | CoverageEligibilityRequestItem | CoverageEligibilityRequestItemDiagnosis | CoverageEligibilityRequestSupportingInfo | CoverageEligibilityResponse | CoverageEligibilityResponseError | CoverageEligibilityResponseInsurance | CoverageEligibilityResponseInsuranceItem | CoverageEligibilityResponseInsuranceItemBenefit | DataRequirement | DataRequirementCodeFilter | DataRequirementDateFilter | DataRequirementSort | DetectedIssue | DetectedIssueEvidence | DetectedIssueMitigation | Device | DeviceDefinition | DeviceDefinitionCapability | DeviceDefinitionClassification | DeviceDefinitionDeviceName | DeviceDefinitionMaterial | DeviceDefinitionProperty | DeviceDefinitionSpecialization | DeviceDefinitionUdiDeviceIdentifier | DeviceDeviceName | DeviceMetric | DeviceMetricCalibration | DeviceProperty | DeviceRequest | DeviceRequestParameter | DeviceSpecialization | DeviceUdiCarrier | DeviceUseStatement | DeviceVersion | DiagnosticReport | DiagnosticReportMedia | Distance | DocumentManifest | DocumentManifestRelated | DocumentReference | DocumentReferenceContent | DocumentReferenceContext | DocumentReferenceRelatesTo | DomainConfiguration | Dosage | DosageDoseAndRate | Duration | EffectEvidenceSynthesis | EffectEvidenceSynthesisCertainty | EffectEvidenceSynthesisCertaintyCertaintySubcomponent | EffectEvidenceSynthesisEffectEstimate | EffectEvidenceSynthesisEffectEstimatePrecisionEstimate | EffectEvidenceSynthesisResultsByExposure | EffectEvidenceSynthesisSampleSize | Element | ElementDefinition | ElementDefinitionBase | ElementDefinitionBinding | ElementDefinitionConstraint | ElementDefinitionExample | ElementDefinitionMapping | ElementDefinitionSlicing | ElementDefinitionSlicingDiscriminator | ElementDefinitionType | Encounter | EncounterClassHistory | EncounterDiagnosis | EncounterHospitalization | EncounterLocation | EncounterParticipant | EncounterStatusHistory | Endpoint | EnrollmentRequest | EnrollmentResponse | EpisodeOfCare | EpisodeOfCareDiagnosis | EpisodeOfCareStatusHistory | EventDefinition | Evidence | EvidenceVariable | EvidenceVariableCharacteristic | EvidenceVariableCharacteristicDefinitionByCombination | EvidenceVariableCharacteristicDefinitionByTypeAndValue | EvidenceVariableCharacteristicTimeFromEvent | ExampleScenario | ExampleScenarioActor | ExampleScenarioInstance | ExampleScenarioInstanceContainedInstance | ExampleScenarioInstanceVersion | ExampleScenarioProcess | ExampleScenarioProcessStep | ExampleScenarioProcessStepAlternative | ExampleScenarioProcessStepOperation | ExplanationOfBenefit | ExplanationOfBenefitAccident | ExplanationOfBenefitAddItem | ExplanationOfBenefitAddItemDetail | ExplanationOfBenefitAddItemDetailSubDetail | ExplanationOfBenefitBenefitBalance | ExplanationOfBenefitBenefitBalanceFinancial | ExplanationOfBenefitCareTeam | ExplanationOfBenefitDiagnosis | ExplanationOfBenefitInsurance | ExplanationOfBenefitItem | ExplanationOfBenefitItemAdjudication | ExplanationOfBenefitItemDetail | ExplanationOfBenefitItemDetailSubDetail | ExplanationOfBenefitPayee | ExplanationOfBenefitPayment | ExplanationOfBenefitProcedure | ExplanationOfBenefitProcessNote | ExplanationOfBenefitRelated | ExplanationOfBenefitSupportingInfo | ExplanationOfBenefitTotal | Expression | Extension | FamilyMemberHistory | FamilyMemberHistoryCondition | Flag | Goal | GoalTarget | GraphDefinition | GraphDefinitionLink | GraphDefinitionLinkTarget | GraphDefinitionLinkTargetCompartment | Group | GroupCharacteristic | GroupMember | GuidanceResponse | HealthcareService | HealthcareServiceAvailableTime | HealthcareServiceEligibility | HealthcareServiceNotAvailable | HumanName | Identifier | IdentityProvider | ImagingStudy | ImagingStudySeries | ImagingStudySeriesInstance | ImagingStudySeriesPerformer | Immunization | ImmunizationEducation | ImmunizationEvaluation | ImmunizationPerformer | ImmunizationProtocolApplied | ImmunizationReaction | ImmunizationRecommendation | ImmunizationRecommendationRecommendation | ImmunizationRecommendationRecommendationDateCriterion | ImplementationGuide | ImplementationGuideDefinition | ImplementationGuideDefinitionGrouping | ImplementationGuideDefinitionPage | ImplementationGuideDefinitionParameter | ImplementationGuideDefinitionResource | ImplementationGuideDefinitionTemplate | ImplementationGuideDependsOn | ImplementationGuideGlobal | ImplementationGuideManifest | ImplementationGuideManifestPage | ImplementationGuideManifestResource | InsurancePlan | InsurancePlanContact | InsurancePlanCoverage | InsurancePlanCoverageBenefit | InsurancePlanCoverageBenefitLimit | InsurancePlanPlan | InsurancePlanPlanGeneralCost | InsurancePlanPlanSpecificCost | InsurancePlanPlanSpecificCostBenefit | InsurancePlanPlanSpecificCostBenefitCost | Invoice | InvoiceLineItem | InvoiceLineItemPriceComponent | InvoiceParticipant | JsonWebKey | Library | Linkage | LinkageItem | List | ListEntry | Location | LocationHoursOfOperation | LocationPosition | Login | MarketingStatus | Measure | MeasureGroup | MeasureGroupPopulation | MeasureGroupStratifier | MeasureGroupStratifierComponent | MeasureReport | MeasureReportGroup | MeasureReportGroupPopulation | MeasureReportGroupStratifier | MeasureReportGroupStratifierStratum | MeasureReportGroupStratifierStratumComponent | MeasureReportGroupStratifierStratumPopulation | MeasureSupplementalData | Media | Medication | MedicationAdministration | MedicationAdministrationDosage | MedicationAdministrationPerformer | MedicationBatch | MedicationDispense | MedicationDispensePerformer | MedicationDispenseSubstitution | MedicationIngredient | MedicationKnowledge | MedicationKnowledgeAdministrationGuidelines | MedicationKnowledgeAdministrationGuidelinesDosage | MedicationKnowledgeAdministrationGuidelinesPatientCharacteristics | MedicationKnowledgeCost | MedicationKnowledgeDrugCharacteristic | MedicationKnowledgeIngredient | MedicationKnowledgeKinetics | MedicationKnowledgeMedicineClassification | MedicationKnowledgeMonitoringProgram | MedicationKnowledgeMonograph | MedicationKnowledgePackaging | MedicationKnowledgeRegulatory | MedicationKnowledgeRegulatoryMaxDispense | MedicationKnowledgeRegulatorySchedule | MedicationKnowledgeRegulatorySubstitution | MedicationKnowledgeRelatedMedicationKnowledge | MedicationRequest | MedicationRequestDispenseRequest | MedicationRequestDispenseRequestInitialFill | MedicationRequestSubstitution | MedicationStatement | MedicinalProduct | MedicinalProductAuthorization | MedicinalProductAuthorizationJurisdictionalAuthorization | MedicinalProductAuthorizationProcedure | MedicinalProductContraindication | MedicinalProductContraindicationOtherTherapy | MedicinalProductIndication | MedicinalProductIndicationOtherTherapy | MedicinalProductIngredient | MedicinalProductIngredientSpecifiedSubstance | MedicinalProductIngredientSpecifiedSubstanceStrength | MedicinalProductIngredientSpecifiedSubstanceStrengthReferenceStrength | MedicinalProductIngredientSubstance | MedicinalProductInteraction | MedicinalProductInteractionInteractant | MedicinalProductManufactured | MedicinalProductManufacturingBusinessOperation | MedicinalProductName | MedicinalProductNameCountryLanguage | MedicinalProductNameNamePart | MedicinalProductPackaged | MedicinalProductPackagedBatchIdentifier | MedicinalProductPackagedPackageItem | MedicinalProductPharmaceutical | MedicinalProductPharmaceuticalCharacteristics | MedicinalProductPharmaceuticalRouteOfAdministration | MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpecies | MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpeciesWithdrawalPeriod | MedicinalProductSpecialDesignation | MedicinalProductUndesirableEffect | MessageDefinition | MessageDefinitionAllowedResponse | MessageDefinitionFocus | MessageHeader | MessageHeaderDestination | MessageHeaderResponse | MessageHeaderSource | Meta | MetadataResource | MolecularSequence | MolecularSequenceQuality | MolecularSequenceQualityRoc | MolecularSequenceReferenceSeq | MolecularSequenceRepository | MolecularSequenceStructureVariant | MolecularSequenceStructureVariantInner | MolecularSequenceStructureVariantOuter | MolecularSequenceVariant | Money | MoneyQuantity | NamingSystem | NamingSystemUniqueId | Narrative | NutritionOrder | NutritionOrderEnteralFormula | NutritionOrderEnteralFormulaAdministration | NutritionOrderOralDiet | NutritionOrderOralDietNutrient | NutritionOrderOralDietTexture | NutritionOrderSupplement | Observation | ObservationComponent | ObservationDefinition | ObservationDefinitionQualifiedInterval | ObservationDefinitionQuantitativeDetails | ObservationReferenceRange | OperationDefinition | OperationDefinitionOverload | OperationDefinitionParameter | OperationDefinitionParameterBinding | OperationDefinitionParameterReferencedFrom | OperationOutcome | OperationOutcomeIssue | Organization | OrganizationAffiliation | OrganizationContact | ParameterDefinition | Parameters | ParametersParameter | PasswordChangeRequest | Patient | PatientCommunication | PatientContact | PatientLink | PaymentNotice | PaymentReconciliation | PaymentReconciliationDetail | PaymentReconciliationProcessNote | Period | Person | PersonLink | PlanDefinition | PlanDefinitionAction | PlanDefinitionActionCondition | PlanDefinitionActionDynamicValue | PlanDefinitionActionParticipant | PlanDefinitionActionRelatedAction | PlanDefinitionGoal | PlanDefinitionGoalTarget | Population | Practitioner | PractitionerQualification | PractitionerRole | PractitionerRoleAvailableTime | PractitionerRoleNotAvailable | Procedure | ProcedureFocalDevice | ProcedurePerformer | ProdCharacteristic | ProductShelfLife | Project | ProjectDefaultProfile | ProjectLink | ProjectMembership | ProjectMembershipAccess | ProjectMembershipAccessParameter | ProjectSetting | ProjectSite | Provenance | ProvenanceAgent | ProvenanceEntity | Quantity | Questionnaire | QuestionnaireItem | QuestionnaireItemAnswerOption | QuestionnaireItemEnableWhen | QuestionnaireItemInitial | QuestionnaireResponse | QuestionnaireResponseItem | QuestionnaireResponseItemAnswer | Range | Ratio | Reference | RelatedArtifact | RelatedPerson | RelatedPersonCommunication | RequestGroup | RequestGroupAction | RequestGroupActionCondition | RequestGroupActionRelatedAction | ResearchDefinition | ResearchElementDefinition | ResearchElementDefinitionCharacteristic | ResearchStudy | ResearchStudyArm | ResearchStudyAssociatedParty | ResearchStudyComparisonGroup | ResearchStudyLabel | ResearchStudyObjective | ResearchStudyOutcomeMeasure | ResearchStudyProgressStatus | ResearchStudyRecruitment | ResearchSubject | RiskAssessment | RiskAssessmentPrediction | RiskEvidenceSynthesis | RiskEvidenceSynthesisCertainty | RiskEvidenceSynthesisCertaintyCertaintySubcomponent | RiskEvidenceSynthesisRiskEstimate | RiskEvidenceSynthesisRiskEstimatePrecisionEstimate | RiskEvidenceSynthesisSampleSize | SampledData | Schedule | SearchParameter | SearchParameterComponent | ServiceRequest | Signature | SimpleQuantity | Slot | SmartAppLaunch | Specimen | SpecimenCollection | SpecimenContainer | SpecimenDefinition | SpecimenDefinitionTypeTested | SpecimenDefinitionTypeTestedContainer | SpecimenDefinitionTypeTestedContainerAdditive | SpecimenDefinitionTypeTestedHandling | SpecimenProcessing | StructureDefinition | StructureDefinitionContext | StructureDefinitionDifferential | StructureDefinitionMapping | StructureDefinitionSnapshot | StructureMap | StructureMapGroup | StructureMapGroupInput | StructureMapGroupRule | StructureMapGroupRuleDependent | StructureMapGroupRuleSource | StructureMapGroupRuleTarget | StructureMapGroupRuleTargetParameter | StructureMapStructure | Subscription | SubscriptionChannel | SubscriptionStatus | SubscriptionStatusNotificationEvent | Substance | SubstanceAmount | SubstanceAmountReferenceRange | SubstanceIngredient | SubstanceInstance | SubstanceNucleicAcid | SubstanceNucleicAcidSubunit | SubstanceNucleicAcidSubunitLinkage | SubstanceNucleicAcidSubunitSugar | SubstancePolymer | SubstancePolymerMonomerSet | SubstancePolymerMonomerSetStartingMaterial | SubstancePolymerRepeat | SubstancePolymerRepeatRepeatUnit | SubstancePolymerRepeatRepeatUnitDegreeOfPolymerisation | SubstancePolymerRepeatRepeatUnitStructuralRepresentation | SubstanceProtein | SubstanceProteinSubunit | SubstanceReferenceInformation | SubstanceReferenceInformationClassification | SubstanceReferenceInformationGene | SubstanceReferenceInformationGeneElement | SubstanceReferenceInformationTarget | SubstanceSourceMaterial | SubstanceSourceMaterialFractionDescription | SubstanceSourceMaterialOrganism | SubstanceSourceMaterialOrganismAuthor | SubstanceSourceMaterialOrganismHybrid | SubstanceSourceMaterialOrganismOrganismGeneral | SubstanceSourceMaterialPartDescription | SubstanceSpecification | SubstanceSpecificationCode | SubstanceSpecificationMoiety | SubstanceSpecificationName | SubstanceSpecificationNameOfficial | SubstanceSpecificationProperty | SubstanceSpecificationRelationship | SubstanceSpecificationStructure | SubstanceSpecificationStructureIsotope | SubstanceSpecificationStructureIsotopeMolecularWeight | SubstanceSpecificationStructureRepresentation | SupplyDelivery | SupplyDeliverySuppliedItem | SupplyRequest | SupplyRequestParameter | Task | TaskInput | TaskOutput | TaskRestriction | TerminologyCapabilities | TerminologyCapabilitiesClosure | TerminologyCapabilitiesCodeSystem | TerminologyCapabilitiesCodeSystemVersion | TerminologyCapabilitiesCodeSystemVersionFilter | TerminologyCapabilitiesExpansion | TerminologyCapabilitiesExpansionParameter | TerminologyCapabilitiesImplementation | TerminologyCapabilitiesSoftware | TerminologyCapabilitiesTranslation | TerminologyCapabilitiesValidateCode | TestReport | TestReportParticipant | TestReportSetup | TestReportSetupAction | TestReportSetupActionAssert | TestReportSetupActionOperation | TestReportTeardown | TestReportTeardownAction | TestReportTest | TestReportTestAction | TestScript | TestScriptDestination | TestScriptFixture | TestScriptMetadata | TestScriptMetadataCapability | TestScriptMetadataLink | TestScriptOrigin | TestScriptSetup | TestScriptSetupAction | TestScriptSetupActionAssert | TestScriptSetupActionOperation | TestScriptSetupActionOperationRequestHeader | TestScriptTeardown | TestScriptTeardownAction | TestScriptTest | TestScriptTestAction | TestScriptVariable | Timing | TimingRepeat | TriggerDefinition | UsageContext | User | UserConfiguration | UserConfigurationMenu | UserConfigurationMenuLink | UserConfigurationOption | UserConfigurationSearch | UserSecurityRequest | ValueSet | ValueSetCompose | ValueSetComposeInclude | ValueSetComposeIncludeConcept | ValueSetComposeIncludeConceptDesignation | ValueSetComposeIncludeFilter | ValueSetExpansion | ValueSetExpansionContains | ValueSetExpansionParameter | VerificationResult | VerificationResultAttestation | VerificationResultPrimarySource | VerificationResultValidator | ViewDefinition | ViewDefinitionConstant | ViewDefinitionSelect | ViewDefinitionSelectColumn | ViewDefinitionSelectColumnTag | ViewDefinitionWhere | VisionPrescription | VisionPrescriptionLensSpecification | VisionPrescriptionLensSpecificationPrism
else:
    # At runtime, use Any to avoid circular import issues
    Resource = Any

__all__ = ["Resource", "ResourceType"]

# Initialize models after all modules are imported
# Import all modules to register their models
from pymedplum.fhir import accesspolicy  # noqa: F401
from pymedplum.fhir import account  # noqa: F401
from pymedplum.fhir import activitydefinition  # noqa: F401
from pymedplum.fhir import address  # noqa: F401
from pymedplum.fhir import adverseevent  # noqa: F401
from pymedplum.fhir import age  # noqa: F401
from pymedplum.fhir import agent  # noqa: F401
from pymedplum.fhir import allergyintolerance  # noqa: F401
from pymedplum.fhir import annotation  # noqa: F401
from pymedplum.fhir import appointment  # noqa: F401
from pymedplum.fhir import appointmentresponse  # noqa: F401
from pymedplum.fhir import asyncjob  # noqa: F401
from pymedplum.fhir import attachment  # noqa: F401
from pymedplum.fhir import auditevent  # noqa: F401
from pymedplum.fhir import backboneelement  # noqa: F401
from pymedplum.fhir import basic  # noqa: F401
from pymedplum.fhir import binary  # noqa: F401
from pymedplum.fhir import biologicallyderivedproduct  # noqa: F401
from pymedplum.fhir import bodystructure  # noqa: F401
from pymedplum.fhir import bot  # noqa: F401
from pymedplum.fhir import bulkdataexport  # noqa: F401
from pymedplum.fhir import bundle  # noqa: F401
from pymedplum.fhir import capabilitystatement  # noqa: F401
from pymedplum.fhir import careplan  # noqa: F401
from pymedplum.fhir import careteam  # noqa: F401
from pymedplum.fhir import catalogentry  # noqa: F401
from pymedplum.fhir import chargeitem  # noqa: F401
from pymedplum.fhir import chargeitemdefinition  # noqa: F401
from pymedplum.fhir import claim  # noqa: F401
from pymedplum.fhir import claimresponse  # noqa: F401
from pymedplum.fhir import clientapplication  # noqa: F401
from pymedplum.fhir import clinicalimpression  # noqa: F401
from pymedplum.fhir import codeableconcept  # noqa: F401
from pymedplum.fhir import codesystem  # noqa: F401
from pymedplum.fhir import coding  # noqa: F401
from pymedplum.fhir import communication  # noqa: F401
from pymedplum.fhir import communicationrequest  # noqa: F401
from pymedplum.fhir import compartmentdefinition  # noqa: F401
from pymedplum.fhir import composition  # noqa: F401
from pymedplum.fhir import conceptmap  # noqa: F401
from pymedplum.fhir import condition  # noqa: F401
from pymedplum.fhir import consent  # noqa: F401
from pymedplum.fhir import contactdetail  # noqa: F401
from pymedplum.fhir import contactpoint  # noqa: F401
from pymedplum.fhir import contract  # noqa: F401
from pymedplum.fhir import contributor  # noqa: F401
from pymedplum.fhir import count  # noqa: F401
from pymedplum.fhir import coverage  # noqa: F401
from pymedplum.fhir import coverageeligibilityrequest  # noqa: F401
from pymedplum.fhir import coverageeligibilityresponse  # noqa: F401
from pymedplum.fhir import datarequirement  # noqa: F401
from pymedplum.fhir import detectedissue  # noqa: F401
from pymedplum.fhir import device  # noqa: F401
from pymedplum.fhir import devicedefinition  # noqa: F401
from pymedplum.fhir import devicemetric  # noqa: F401
from pymedplum.fhir import devicerequest  # noqa: F401
from pymedplum.fhir import deviceusestatement  # noqa: F401
from pymedplum.fhir import diagnosticreport  # noqa: F401
from pymedplum.fhir import distance  # noqa: F401
from pymedplum.fhir import documentmanifest  # noqa: F401
from pymedplum.fhir import documentreference  # noqa: F401
from pymedplum.fhir import domainconfiguration  # noqa: F401
from pymedplum.fhir import dosage  # noqa: F401
from pymedplum.fhir import duration  # noqa: F401
from pymedplum.fhir import effectevidencesynthesis  # noqa: F401
from pymedplum.fhir import element  # noqa: F401
from pymedplum.fhir import elementdefinition  # noqa: F401
from pymedplum.fhir import encounter  # noqa: F401
from pymedplum.fhir import endpoint  # noqa: F401
from pymedplum.fhir import enrollmentrequest  # noqa: F401
from pymedplum.fhir import enrollmentresponse  # noqa: F401
from pymedplum.fhir import episodeofcare  # noqa: F401
from pymedplum.fhir import eventdefinition  # noqa: F401
from pymedplum.fhir import evidence  # noqa: F401
from pymedplum.fhir import evidencevariable  # noqa: F401
from pymedplum.fhir import examplescenario  # noqa: F401
from pymedplum.fhir import explanationofbenefit  # noqa: F401
from pymedplum.fhir import expression  # noqa: F401
from pymedplum.fhir import extension  # noqa: F401
from pymedplum.fhir import familymemberhistory  # noqa: F401
from pymedplum.fhir import flag  # noqa: F401
from pymedplum.fhir import goal  # noqa: F401
from pymedplum.fhir import graphdefinition  # noqa: F401
from pymedplum.fhir import group  # noqa: F401
from pymedplum.fhir import guidanceresponse  # noqa: F401
from pymedplum.fhir import healthcareservice  # noqa: F401
from pymedplum.fhir import humanname  # noqa: F401
from pymedplum.fhir import identifier  # noqa: F401
from pymedplum.fhir import identityprovider  # noqa: F401
from pymedplum.fhir import imagingstudy  # noqa: F401
from pymedplum.fhir import immunization  # noqa: F401
from pymedplum.fhir import immunizationevaluation  # noqa: F401
from pymedplum.fhir import immunizationrecommendation  # noqa: F401
from pymedplum.fhir import implementationguide  # noqa: F401
from pymedplum.fhir import insuranceplan  # noqa: F401
from pymedplum.fhir import invoice  # noqa: F401
from pymedplum.fhir import jsonwebkey  # noqa: F401
from pymedplum.fhir import library  # noqa: F401
from pymedplum.fhir import linkage  # noqa: F401
from pymedplum.fhir import list  # noqa: F401
from pymedplum.fhir import location  # noqa: F401
from pymedplum.fhir import login  # noqa: F401
from pymedplum.fhir import marketingstatus  # noqa: F401
from pymedplum.fhir import measure  # noqa: F401
from pymedplum.fhir import measurereport  # noqa: F401
from pymedplum.fhir import media  # noqa: F401
from pymedplum.fhir import medication  # noqa: F401
from pymedplum.fhir import medicationadministration  # noqa: F401
from pymedplum.fhir import medicationdispense  # noqa: F401
from pymedplum.fhir import medicationknowledge  # noqa: F401
from pymedplum.fhir import medicationrequest  # noqa: F401
from pymedplum.fhir import medicationstatement  # noqa: F401
from pymedplum.fhir import medicinalproduct  # noqa: F401
from pymedplum.fhir import medicinalproductauthorization  # noqa: F401
from pymedplum.fhir import medicinalproductcontraindication  # noqa: F401
from pymedplum.fhir import medicinalproductindication  # noqa: F401
from pymedplum.fhir import medicinalproductingredient  # noqa: F401
from pymedplum.fhir import medicinalproductinteraction  # noqa: F401
from pymedplum.fhir import medicinalproductmanufactured  # noqa: F401
from pymedplum.fhir import medicinalproductpackaged  # noqa: F401
from pymedplum.fhir import medicinalproductpharmaceutical  # noqa: F401
from pymedplum.fhir import medicinalproductundesirableeffect  # noqa: F401
from pymedplum.fhir import messagedefinition  # noqa: F401
from pymedplum.fhir import messageheader  # noqa: F401
from pymedplum.fhir import meta  # noqa: F401
from pymedplum.fhir import metadataresource  # noqa: F401
from pymedplum.fhir import molecularsequence  # noqa: F401
from pymedplum.fhir import money  # noqa: F401
from pymedplum.fhir import moneyquantity  # noqa: F401
from pymedplum.fhir import namingsystem  # noqa: F401
from pymedplum.fhir import narrative  # noqa: F401
from pymedplum.fhir import nutritionorder  # noqa: F401
from pymedplum.fhir import observation  # noqa: F401
from pymedplum.fhir import observationdefinition  # noqa: F401
from pymedplum.fhir import operationdefinition  # noqa: F401
from pymedplum.fhir import operationoutcome  # noqa: F401
from pymedplum.fhir import organization  # noqa: F401
from pymedplum.fhir import organizationaffiliation  # noqa: F401
from pymedplum.fhir import parameterdefinition  # noqa: F401
from pymedplum.fhir import parameters  # noqa: F401
from pymedplum.fhir import passwordchangerequest  # noqa: F401
from pymedplum.fhir import patient  # noqa: F401
from pymedplum.fhir import paymentnotice  # noqa: F401
from pymedplum.fhir import paymentreconciliation  # noqa: F401
from pymedplum.fhir import period  # noqa: F401
from pymedplum.fhir import person  # noqa: F401
from pymedplum.fhir import plandefinition  # noqa: F401
from pymedplum.fhir import population  # noqa: F401
from pymedplum.fhir import practitioner  # noqa: F401
from pymedplum.fhir import practitionerrole  # noqa: F401
from pymedplum.fhir import procedure  # noqa: F401
from pymedplum.fhir import prodcharacteristic  # noqa: F401
from pymedplum.fhir import productshelflife  # noqa: F401
from pymedplum.fhir import project  # noqa: F401
from pymedplum.fhir import projectmembership  # noqa: F401
from pymedplum.fhir import provenance  # noqa: F401
from pymedplum.fhir import quantity  # noqa: F401
from pymedplum.fhir import questionnaire  # noqa: F401
from pymedplum.fhir import questionnaireresponse  # noqa: F401
from pymedplum.fhir import range  # noqa: F401
from pymedplum.fhir import ratio  # noqa: F401
from pymedplum.fhir import reference  # noqa: F401
from pymedplum.fhir import relatedartifact  # noqa: F401
from pymedplum.fhir import relatedperson  # noqa: F401
from pymedplum.fhir import requestgroup  # noqa: F401
from pymedplum.fhir import researchdefinition  # noqa: F401
from pymedplum.fhir import researchelementdefinition  # noqa: F401
from pymedplum.fhir import researchstudy  # noqa: F401
from pymedplum.fhir import researchsubject  # noqa: F401
from pymedplum.fhir import riskassessment  # noqa: F401
from pymedplum.fhir import riskevidencesynthesis  # noqa: F401
from pymedplum.fhir import sampleddata  # noqa: F401
from pymedplum.fhir import schedule  # noqa: F401
from pymedplum.fhir import searchparameter  # noqa: F401
from pymedplum.fhir import servicerequest  # noqa: F401
from pymedplum.fhir import signature  # noqa: F401
from pymedplum.fhir import simplequantity  # noqa: F401
from pymedplum.fhir import slot  # noqa: F401
from pymedplum.fhir import smartapplaunch  # noqa: F401
from pymedplum.fhir import specimen  # noqa: F401
from pymedplum.fhir import specimendefinition  # noqa: F401
from pymedplum.fhir import structuredefinition  # noqa: F401
from pymedplum.fhir import structuremap  # noqa: F401
from pymedplum.fhir import subscription  # noqa: F401
from pymedplum.fhir import subscriptionstatus  # noqa: F401
from pymedplum.fhir import substance  # noqa: F401
from pymedplum.fhir import substanceamount  # noqa: F401
from pymedplum.fhir import substancenucleicacid  # noqa: F401
from pymedplum.fhir import substancepolymer  # noqa: F401
from pymedplum.fhir import substanceprotein  # noqa: F401
from pymedplum.fhir import substancereferenceinformation  # noqa: F401
from pymedplum.fhir import substancesourcematerial  # noqa: F401
from pymedplum.fhir import substancespecification  # noqa: F401
from pymedplum.fhir import supplydelivery  # noqa: F401
from pymedplum.fhir import supplyrequest  # noqa: F401
from pymedplum.fhir import task  # noqa: F401
from pymedplum.fhir import terminologycapabilities  # noqa: F401
from pymedplum.fhir import testreport  # noqa: F401
from pymedplum.fhir import testscript  # noqa: F401
from pymedplum.fhir import timing  # noqa: F401
from pymedplum.fhir import triggerdefinition  # noqa: F401
from pymedplum.fhir import usagecontext  # noqa: F401
from pymedplum.fhir import user  # noqa: F401
from pymedplum.fhir import userconfiguration  # noqa: F401
from pymedplum.fhir import usersecurityrequest  # noqa: F401
from pymedplum.fhir import valueset  # noqa: F401
from pymedplum.fhir import verificationresult  # noqa: F401
from pymedplum.fhir import viewdefinition  # noqa: F401
from pymedplum.fhir import visionprescription  # noqa: F401

# Register special types and typing constructs for forward reference resolution
from typing import Dict as typing_Dict, List as typing_List
from pymedplum.fhir._rebuild import register_model

# Register typing constructs first (they should override FHIR classes with same names)
register_model('List', typing_List)
register_model('Dict', typing_Dict)

# Register special FHIR type aliases
register_model('Resource', Resource)
register_model('ResourceType', ResourceType)

# Rebuild all models to resolve forward references
from pymedplum.fhir._rebuild import rebuild_all_models
rebuild_all_models()
