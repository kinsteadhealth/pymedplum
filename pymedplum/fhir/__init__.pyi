"""Type stubs for pymedplum.fhir module.
This is a generated file.
Do not edit it manually

Pylance uses imports to provide autocomplete for all FHIR resources.
The lazy loader (__getattr__) handles actual imports at runtime.
"""

# ruff: noqa: F822

from typing import Any

# Type imports for IDE autocomplete
from .accesspolicy import AccessPolicy, AccessPolicyIpAccessRule, AccessPolicyResource
from .account import Account, AccountCoverage, AccountGuarantor
from .activitydefinition import (
    ActivityDefinition,
    ActivityDefinitionDynamicValue,
    ActivityDefinitionParticipant,
)
from .address import Address
from .adverseevent import (
    AdverseEvent,
    AdverseEventSuspectEntity,
    AdverseEventSuspectEntityCausality,
)
from .age import Age
from .agent import Agent, AgentChannel, AgentSetting
from .allergyintolerance import AllergyIntolerance, AllergyIntoleranceReaction
from .annotation import Annotation
from .appointment import Appointment, AppointmentParticipant
from .appointmentresponse import AppointmentResponse
from .asyncjob import AsyncJob
from .attachment import Attachment
from .auditevent import (
    AuditEvent,
    AuditEventAgent,
    AuditEventAgentNetwork,
    AuditEventEntity,
    AuditEventEntityDetail,
    AuditEventSource,
)
from .backboneelement import BackboneElement
from .basic import Basic
from .binary import Binary
from .biologicallyderivedproduct import (
    BiologicallyDerivedProduct,
    BiologicallyDerivedProductCollection,
    BiologicallyDerivedProductManipulation,
    BiologicallyDerivedProductProcessing,
    BiologicallyDerivedProductStorage,
)
from .bodystructure import BodyStructure
from .bot import Bot, BotCdsService, BotCdsServicePrefetch
from .bulkdataexport import (
    BulkDataExport,
    BulkDataExportDeleted,
    BulkDataExportError,
    BulkDataExportOutput,
)
from .bundle import (
    Bundle,
    BundleEntry,
    BundleEntryRequest,
    BundleEntryResponse,
    BundleEntrySearch,
    BundleLink,
)
from .capabilitystatement import (
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
from .careplan import CarePlan, CarePlanActivity, CarePlanActivityDetail
from .careteam import CareTeam, CareTeamParticipant
from .catalogentry import CatalogEntry, CatalogEntryRelatedEntry
from .chargeitem import ChargeItem, ChargeItemPerformer
from .chargeitemdefinition import (
    ChargeItemDefinition,
    ChargeItemDefinitionApplicability,
    ChargeItemDefinitionPropertyGroup,
    ChargeItemDefinitionPropertyGroupPriceComponent,
)
from .claim import (
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
from .claimresponse import (
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
from .clientapplication import (
    ClientApplication,
    ClientApplicationLaunchIdentifierSystems,
    ClientApplicationSignInForm,
)
from .clinicalimpression import (
    ClinicalImpression,
    ClinicalImpressionFinding,
    ClinicalImpressionInvestigation,
)
from .codeableconcept import CodeableConcept
from .codesystem import (
    CodeSystem,
    CodeSystemConcept,
    CodeSystemConceptDesignation,
    CodeSystemConceptProperty,
    CodeSystemFilter,
    CodeSystemProperty,
)
from .coding import Coding
from .communication import Communication, CommunicationPayload
from .communicationrequest import CommunicationRequest, CommunicationRequestPayload
from .compartmentdefinition import CompartmentDefinition, CompartmentDefinitionResource
from .composition import (
    Composition,
    CompositionAttester,
    CompositionEvent,
    CompositionRelatesTo,
    CompositionSection,
)
from .conceptmap import (
    ConceptMap,
    ConceptMapGroup,
    ConceptMapGroupElement,
    ConceptMapGroupElementTarget,
    ConceptMapGroupElementTargetDependsOn,
    ConceptMapGroupUnmapped,
)
from .condition import Condition, ConditionEvidence, ConditionStage
from .consent import (
    Consent,
    ConsentPolicy,
    ConsentProvision,
    ConsentProvisionActor,
    ConsentProvisionData,
    ConsentVerification,
)
from .contactdetail import ContactDetail
from .contactpoint import ContactPoint
from .contract import (
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
from .contributor import Contributor
from .count import Count
from .coverage import (
    Coverage,
    CoverageClass,
    CoverageCostToBeneficiary,
    CoverageCostToBeneficiaryException,
)
from .coverageeligibilityrequest import (
    CoverageEligibilityRequest,
    CoverageEligibilityRequestInsurance,
    CoverageEligibilityRequestItem,
    CoverageEligibilityRequestItemDiagnosis,
    CoverageEligibilityRequestSupportingInfo,
)
from .coverageeligibilityresponse import (
    CoverageEligibilityResponse,
    CoverageEligibilityResponseError,
    CoverageEligibilityResponseInsurance,
    CoverageEligibilityResponseInsuranceItem,
    CoverageEligibilityResponseInsuranceItemBenefit,
)
from .datarequirement import (
    DataRequirement,
    DataRequirementCodeFilter,
    DataRequirementDateFilter,
    DataRequirementSort,
)
from .detectedissue import DetectedIssue, DetectedIssueEvidence, DetectedIssueMitigation
from .device import (
    Device,
    DeviceDeviceName,
    DeviceProperty,
    DeviceSpecialization,
    DeviceUdiCarrier,
    DeviceVersion,
)
from .devicedefinition import (
    DeviceDefinition,
    DeviceDefinitionCapability,
    DeviceDefinitionClassification,
    DeviceDefinitionDeviceName,
    DeviceDefinitionMaterial,
    DeviceDefinitionProperty,
    DeviceDefinitionSpecialization,
    DeviceDefinitionUdiDeviceIdentifier,
)
from .devicemetric import DeviceMetric, DeviceMetricCalibration
from .devicerequest import DeviceRequest, DeviceRequestParameter
from .deviceusestatement import DeviceUseStatement
from .diagnosticreport import DiagnosticReport, DiagnosticReportMedia
from .distance import Distance
from .documentmanifest import DocumentManifest, DocumentManifestRelated
from .documentreference import (
    DocumentReference,
    DocumentReferenceContent,
    DocumentReferenceContext,
    DocumentReferenceRelatesTo,
)
from .domainconfiguration import DomainConfiguration
from .dosage import Dosage, DosageDoseAndRate
from .duration import Duration
from .effectevidencesynthesis import (
    EffectEvidenceSynthesis,
    EffectEvidenceSynthesisCertainty,
    EffectEvidenceSynthesisCertaintyCertaintySubcomponent,
    EffectEvidenceSynthesisEffectEstimate,
    EffectEvidenceSynthesisEffectEstimatePrecisionEstimate,
    EffectEvidenceSynthesisResultsByExposure,
    EffectEvidenceSynthesisSampleSize,
)
from .element import Element
from .elementdefinition import (
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
from .encounter import (
    Encounter,
    EncounterClassHistory,
    EncounterDiagnosis,
    EncounterHospitalization,
    EncounterLocation,
    EncounterParticipant,
    EncounterStatusHistory,
)
from .endpoint import Endpoint
from .enrollmentrequest import EnrollmentRequest
from .enrollmentresponse import EnrollmentResponse
from .episodeofcare import (
    EpisodeOfCare,
    EpisodeOfCareDiagnosis,
    EpisodeOfCareStatusHistory,
)
from .eventdefinition import EventDefinition
from .evidence import Evidence
from .evidencevariable import (
    EvidenceVariable,
    EvidenceVariableCharacteristic,
    EvidenceVariableCharacteristicDefinitionByCombination,
    EvidenceVariableCharacteristicDefinitionByTypeAndValue,
    EvidenceVariableCharacteristicTimeFromEvent,
)
from .examplescenario import (
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
from .explanationofbenefit import (
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
from .expression import Expression
from .extension import Extension
from .familymemberhistory import FamilyMemberHistory, FamilyMemberHistoryCondition
from .flag import Flag
from .goal import Goal, GoalTarget
from .graphdefinition import (
    GraphDefinition,
    GraphDefinitionLink,
    GraphDefinitionLinkTarget,
    GraphDefinitionLinkTargetCompartment,
)
from .group import Group, GroupCharacteristic, GroupMember
from .guidanceresponse import GuidanceResponse
from .healthcareservice import (
    HealthcareService,
    HealthcareServiceAvailableTime,
    HealthcareServiceEligibility,
    HealthcareServiceNotAvailable,
)
from .humanname import HumanName
from .identifier import Identifier
from .identityprovider import IdentityProvider
from .imagingstudy import (
    ImagingStudy,
    ImagingStudySeries,
    ImagingStudySeriesInstance,
    ImagingStudySeriesPerformer,
)
from .immunization import (
    Immunization,
    ImmunizationEducation,
    ImmunizationPerformer,
    ImmunizationProtocolApplied,
    ImmunizationReaction,
)
from .immunizationevaluation import ImmunizationEvaluation
from .immunizationrecommendation import (
    ImmunizationRecommendation,
    ImmunizationRecommendationRecommendation,
    ImmunizationRecommendationRecommendationDateCriterion,
)
from .implementationguide import (
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
from .insuranceplan import (
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
from .invoice import (
    Invoice,
    InvoiceLineItem,
    InvoiceLineItemPriceComponent,
    InvoiceParticipant,
)
from .jsonwebkey import JsonWebKey
from .library import Library
from .linkage import Linkage, LinkageItem
from .list import List, ListEntry
from .location import Location, LocationHoursOfOperation, LocationPosition
from .login import Login
from .marketingstatus import MarketingStatus
from .measure import (
    Measure,
    MeasureGroup,
    MeasureGroupPopulation,
    MeasureGroupStratifier,
    MeasureGroupStratifierComponent,
    MeasureSupplementalData,
)
from .measurereport import (
    MeasureReport,
    MeasureReportGroup,
    MeasureReportGroupPopulation,
    MeasureReportGroupStratifier,
    MeasureReportGroupStratifierStratum,
    MeasureReportGroupStratifierStratumComponent,
    MeasureReportGroupStratifierStratumPopulation,
)
from .media import Media
from .medication import Medication, MedicationBatch, MedicationIngredient
from .medicationadministration import (
    MedicationAdministration,
    MedicationAdministrationDosage,
    MedicationAdministrationPerformer,
)
from .medicationdispense import (
    MedicationDispense,
    MedicationDispensePerformer,
    MedicationDispenseSubstitution,
)
from .medicationknowledge import (
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
from .medicationrequest import (
    MedicationRequest,
    MedicationRequestDispenseRequest,
    MedicationRequestDispenseRequestInitialFill,
    MedicationRequestSubstitution,
)
from .medicationstatement import MedicationStatement
from .medicinalproduct import (
    MedicinalProduct,
    MedicinalProductManufacturingBusinessOperation,
    MedicinalProductName,
    MedicinalProductNameCountryLanguage,
    MedicinalProductNameNamePart,
    MedicinalProductSpecialDesignation,
)
from .medicinalproductauthorization import (
    MedicinalProductAuthorization,
    MedicinalProductAuthorizationJurisdictionalAuthorization,
    MedicinalProductAuthorizationProcedure,
)
from .medicinalproductcontraindication import (
    MedicinalProductContraindication,
    MedicinalProductContraindicationOtherTherapy,
)
from .medicinalproductindication import (
    MedicinalProductIndication,
    MedicinalProductIndicationOtherTherapy,
)
from .medicinalproductingredient import (
    MedicinalProductIngredient,
    MedicinalProductIngredientSpecifiedSubstance,
    MedicinalProductIngredientSpecifiedSubstanceStrength,
    MedicinalProductIngredientSpecifiedSubstanceStrengthReferenceStrength,
    MedicinalProductIngredientSubstance,
)
from .medicinalproductinteraction import (
    MedicinalProductInteraction,
    MedicinalProductInteractionInteractant,
)
from .medicinalproductmanufactured import MedicinalProductManufactured
from .medicinalproductpackaged import (
    MedicinalProductPackaged,
    MedicinalProductPackagedBatchIdentifier,
    MedicinalProductPackagedPackageItem,
)
from .medicinalproductpharmaceutical import (
    MedicinalProductPharmaceutical,
    MedicinalProductPharmaceuticalCharacteristics,
    MedicinalProductPharmaceuticalRouteOfAdministration,
    MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpecies,
    MedicinalProductPharmaceuticalRouteOfAdministrationTargetSpeciesWithdrawalPeriod,
)
from .medicinalproductundesirableeffect import MedicinalProductUndesirableEffect
from .messagedefinition import (
    MessageDefinition,
    MessageDefinitionAllowedResponse,
    MessageDefinitionFocus,
)
from .messageheader import (
    MessageHeader,
    MessageHeaderDestination,
    MessageHeaderResponse,
    MessageHeaderSource,
)
from .meta import Meta
from .metadataresource import MetadataResource
from .molecularsequence import (
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
from .money import Money
from .moneyquantity import MoneyQuantity
from .namingsystem import NamingSystem, NamingSystemUniqueId
from .narrative import Narrative
from .nutritionorder import (
    NutritionOrder,
    NutritionOrderEnteralFormula,
    NutritionOrderEnteralFormulaAdministration,
    NutritionOrderOralDiet,
    NutritionOrderOralDietNutrient,
    NutritionOrderOralDietTexture,
    NutritionOrderSupplement,
)
from .observation import Observation, ObservationComponent, ObservationReferenceRange
from .observationdefinition import (
    ObservationDefinition,
    ObservationDefinitionQualifiedInterval,
    ObservationDefinitionQuantitativeDetails,
)
from .operationdefinition import (
    OperationDefinition,
    OperationDefinitionOverload,
    OperationDefinitionParameter,
    OperationDefinitionParameterBinding,
    OperationDefinitionParameterReferencedFrom,
)
from .operationoutcome import OperationOutcome, OperationOutcomeIssue
from .organization import Organization, OrganizationContact
from .organizationaffiliation import OrganizationAffiliation
from .package import Package
from .packageinstallation import PackageInstallation
from .packagerelease import PackageRelease
from .parameterdefinition import ParameterDefinition
from .parameters import Parameters, ParametersParameter
from .patient import Patient, PatientCommunication, PatientContact, PatientLink
from .paymentnotice import PaymentNotice
from .paymentreconciliation import (
    PaymentReconciliation,
    PaymentReconciliationDetail,
    PaymentReconciliationProcessNote,
)
from .period import Period
from .person import Person, PersonLink
from .plandefinition import (
    PlanDefinition,
    PlanDefinitionAction,
    PlanDefinitionActionCondition,
    PlanDefinitionActionDynamicValue,
    PlanDefinitionActionParticipant,
    PlanDefinitionActionRelatedAction,
    PlanDefinitionGoal,
    PlanDefinitionGoalTarget,
)
from .population import Population
from .practitioner import Practitioner, PractitionerQualification
from .practitionerrole import (
    PractitionerRole,
    PractitionerRoleAvailableTime,
    PractitionerRoleNotAvailable,
)
from .procedure import Procedure, ProcedureFocalDevice, ProcedurePerformer
from .prodcharacteristic import ProdCharacteristic
from .productshelflife import ProductShelfLife
from .project import (
    Project,
    ProjectDefaultProfile,
    ProjectLink,
    ProjectSetting,
    ProjectSite,
)
from .projectmembership import (
    ProjectMembership,
    ProjectMembershipAccess,
    ProjectMembershipAccessParameter,
)
from .provenance import Provenance, ProvenanceAgent, ProvenanceEntity
from .quantity import Quantity
from .questionnaire import (
    Questionnaire,
    QuestionnaireItem,
    QuestionnaireItemAnswerOption,
    QuestionnaireItemEnableWhen,
    QuestionnaireItemInitial,
)
from .questionnaireresponse import (
    QuestionnaireResponse,
    QuestionnaireResponseItem,
    QuestionnaireResponseItemAnswer,
)
from .range import Range
from .ratio import Ratio
from .reference import Reference
from .relatedartifact import RelatedArtifact
from .relatedperson import RelatedPerson, RelatedPersonCommunication
from .requestgroup import (
    RequestGroup,
    RequestGroupAction,
    RequestGroupActionCondition,
    RequestGroupActionRelatedAction,
)
from .researchdefinition import ResearchDefinition
from .researchelementdefinition import (
    ResearchElementDefinition,
    ResearchElementDefinitionCharacteristic,
)
from .researchstudy import (
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
from .researchsubject import ResearchSubject
from .riskassessment import RiskAssessment, RiskAssessmentPrediction
from .riskevidencesynthesis import (
    RiskEvidenceSynthesis,
    RiskEvidenceSynthesisCertainty,
    RiskEvidenceSynthesisCertaintyCertaintySubcomponent,
    RiskEvidenceSynthesisRiskEstimate,
    RiskEvidenceSynthesisRiskEstimatePrecisionEstimate,
    RiskEvidenceSynthesisSampleSize,
)
from .sampleddata import SampledData
from .schedule import Schedule
from .searchparameter import SearchParameter, SearchParameterComponent
from .servicerequest import ServiceRequest
from .signature import Signature
from .simplequantity import SimpleQuantity
from .slot import Slot
from .smartapplaunch import SmartAppLaunch
from .specimen import (
    Specimen,
    SpecimenCollection,
    SpecimenContainer,
    SpecimenProcessing,
)
from .specimendefinition import (
    SpecimenDefinition,
    SpecimenDefinitionTypeTested,
    SpecimenDefinitionTypeTestedContainer,
    SpecimenDefinitionTypeTestedContainerAdditive,
    SpecimenDefinitionTypeTestedHandling,
)
from .structuredefinition import (
    StructureDefinition,
    StructureDefinitionContext,
    StructureDefinitionDifferential,
    StructureDefinitionMapping,
    StructureDefinitionSnapshot,
)
from .structuremap import (
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
from .subscription import Subscription, SubscriptionChannel
from .subscriptionstatus import SubscriptionStatus, SubscriptionStatusNotificationEvent
from .substance import Substance, SubstanceIngredient, SubstanceInstance
from .substanceamount import SubstanceAmount, SubstanceAmountReferenceRange
from .substancenucleicacid import (
    SubstanceNucleicAcid,
    SubstanceNucleicAcidSubunit,
    SubstanceNucleicAcidSubunitLinkage,
    SubstanceNucleicAcidSubunitSugar,
)
from .substancepolymer import (
    SubstancePolymer,
    SubstancePolymerMonomerSet,
    SubstancePolymerMonomerSetStartingMaterial,
    SubstancePolymerRepeat,
    SubstancePolymerRepeatRepeatUnit,
    SubstancePolymerRepeatRepeatUnitDegreeOfPolymerisation,
    SubstancePolymerRepeatRepeatUnitStructuralRepresentation,
)
from .substanceprotein import SubstanceProtein, SubstanceProteinSubunit
from .substancereferenceinformation import (
    SubstanceReferenceInformation,
    SubstanceReferenceInformationClassification,
    SubstanceReferenceInformationGene,
    SubstanceReferenceInformationGeneElement,
    SubstanceReferenceInformationTarget,
)
from .substancesourcematerial import (
    SubstanceSourceMaterial,
    SubstanceSourceMaterialFractionDescription,
    SubstanceSourceMaterialOrganism,
    SubstanceSourceMaterialOrganismAuthor,
    SubstanceSourceMaterialOrganismHybrid,
    SubstanceSourceMaterialOrganismOrganismGeneral,
    SubstanceSourceMaterialPartDescription,
)
from .substancespecification import (
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
from .supplydelivery import SupplyDelivery, SupplyDeliverySuppliedItem
from .supplyrequest import SupplyRequest, SupplyRequestParameter
from .task import Task, TaskInput, TaskOutput, TaskRestriction
from .terminologycapabilities import (
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
from .testreport import (
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
from .testscript import (
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
from .timing import Timing, TimingRepeat
from .triggerdefinition import TriggerDefinition
from .usagecontext import UsageContext
from .user import User
from .userconfiguration import (
    UserConfiguration,
    UserConfigurationMenu,
    UserConfigurationMenuLink,
    UserConfigurationOption,
    UserConfigurationSearch,
)
from .usersecurityrequest import UserSecurityRequest
from .valueset import (
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
from .verificationresult import (
    VerificationResult,
    VerificationResultAttestation,
    VerificationResultPrimarySource,
    VerificationResultValidator,
)
from .viewdefinition import (
    ViewDefinition,
    ViewDefinitionConstant,
    ViewDefinitionSelect,
    ViewDefinitionSelectColumn,
    ViewDefinitionSelectColumnTag,
    ViewDefinitionWhere,
)
from .visionprescription import (
    VisionPrescription,
    VisionPrescriptionLensSpecification,
    VisionPrescriptionLensSpecificationPrism,
)

# Stub for runtime lazy loader
def __getattr__(name: str) -> Any: ...

# Introspection support
def __dir__() -> list[str]: ...

# Explicit exports for IDE autocomplete
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
    "BotCdsService",
    "BotCdsServicePrefetch",
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
    "ClientApplicationLaunchIdentifierSystems",
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
    "Package",
    "PackageInstallation",
    "PackageRelease",
    "ParameterDefinition",
    "Parameters",
    "ParametersParameter",
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
