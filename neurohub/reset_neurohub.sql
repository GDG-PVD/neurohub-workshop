-- Drop indexes first
DROP INDEX IF EXISTS ResearcherByName;
DROP INDEX IF EXISTS ResearcherByInstitution;
DROP INDEX IF EXISTS ExperimentByStatus;
DROP INDEX IF EXISTS ExperimentByPI;
DROP INDEX IF EXISTS DeviceByType;
DROP INDEX IF EXISTS SignalByExperiment;
DROP INDEX IF EXISTS SignalByDevice;
DROP INDEX IF EXISTS SessionByExperiment;
DROP INDEX IF EXISTS AnalysisBySignal;
DROP INDEX IF EXISTS CollaborationByResearcherB;

-- Drop property graph
DROP PROPERTY GRAPH IF EXISTS NeuroResearchGraph;

-- Drop tables (in reverse order of dependencies)
DROP TABLE IF EXISTS Publication;
DROP TABLE IF EXISTS ExperimentDevice;
DROP TABLE IF EXISTS Collaboration;
DROP TABLE IF EXISTS Analysis;
DROP TABLE IF EXISTS SignalData;
DROP TABLE IF EXISTS Session;
DROP TABLE IF EXISTS Device;
DROP TABLE IF EXISTS Experiment;
DROP TABLE IF EXISTS Researcher;