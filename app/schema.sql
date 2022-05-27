DROP TABLE IF EXISTS coexpression;
DROP TABLE IF EXISTS orf;
DROP TABLE IF EXISTS coexpression_network;
DROP TABLE IF EXISTS go_orfs;
DROP TABLE IF EXISTS coexpression_cluster;
DROP TABLE IF EXISTS gene_ontology;
CREATE TABLE orf (
  orf_id INTEGER PRIMARY KEY,
  orf_name VARCHAR(255) NOT NULL,
  -- 
  orf_sequence TEXT NOT NULL,
  orf_start INTEGER NOT NULL,
  orf_end INTEGER NOT NULL,
  orf_strand CHAR(1) NOT NULL,
  orf_length INTEGER NOT NULL,
  orf_gc_content FLOAT NOT NULL,
  orf_riboseq_qvalue FLOAT NOT NULL,
  orf_riboseq_reads INTEGER NOT NULL,
  orf_upstream_neighbor VARCHAR(255) NOT NULL,
  orf_downstream_neighbor VARCHAR(255) NOT NULL,
  orf_upstream_neighbor_distance INTEGER NOT NULL,
  orf_downstream_neighbor_distance INTEGER NOT NULL,
  orf_upstream_neighbor_strand CHAR(1) NOT NULL,
  orf_downstream_neighbor_strand CHAR(1) NOT NULL,
  orf_upstream_neighbor_length INTEGER NOT NULL,
  orf_downstream_neighbor_length INTEGER NOT NULL
);
CREATE TABLE coexpression (
  orf_id INTEGER,
  coexpression_id INTEGER,
  coexpressed_orf_id INTEGER,
  rho FLOAT,
  pairwise_observations INTEGER,
  pearson_r FLOAT,
  spearman_r FLOAT,
  PRIMARY KEY(orf_id, coexpressed_orf_id),
  FOREIGN KEY(coexpressed_orf_id) REFERENCES orf(orf_id),
  FOREIGN KEY(orf_id) REFERENCES orf(orf_id)
);
CREATE TABLE coexpression_network (
  orf_id INTEGER,
  cluster_id INTEGER,
  degree INTEGER,
  FOREIGN KEY(orf_id) REFERENCES orf(orf_id),
  FOREIGN KEY(cluster_id) REFERENCES coexpression_cluster(cluster_id),
  PRIMARY KEY(orf_id, cluster_id)
);
CREATE TABLE go_orfs (
  go_orfs_id INTEGER PRIMARY KEY,
  orf_id INTEGER NOT NULL,
  FOREIGN KEY(orf_id) REFERENCES orf(orf_id)
);
CREATE TABLE coexpression_cluster (
  cluster_id INTEGER PRIMARY KEY,
  cluster_name VARCHAR(255) NOT NULL,
  cluster_size INTEGER NOT NULL,
  transient_ratio FLOAT NOT NULL,
  conserved_ratio FLOAT NOT NULL,
  nei_ratio FLOAT NOT NULL,
  transient_count INTEGER NOT NULL,
  conserved_count INTEGER NOT NULL,
  nei_count INTEGER NOT NULL,
  bp_count INTEGER NOT NULL,
  mf_count INTEGER NOT NULL,
  cc_count INTEGER NOT NULL,
  tf_count INTEGER NOT NULL
);
CREATE TABLE gene_ontology (
  gene_ontology_table_id INTEGER PRIMARY KEY,
  go_name VARCHAR(255) NOT NULL,
  go_id VARCHAR(255) NOT NULL,
  go_definition VARCHAR(255) NOT NULL,
  study_count INTEGER NOT NULL,
  study_ratio FLOAT NOT NULL,
  population_count INTEGER NOT NULL,
  population_ratio FLOAT NOT NULL,
  cluster_id INTEGER NOT NULL,
  study_orfs_id INTEGER NOT NULL,
  FOREIGN KEY(cluster_id) REFERENCES coexpression_cluster(cluster_id),
  FOREIGN KEY(study_orfs_id) REFERENCES go_orfs(go_orfs_id)
);
INSERT INTO orf (
    orf_id,
    orf_name,
    orf_sequence,
    orf_start,
    orf_end,
    orf_strand,
    orf_length,
    orf_gc_content,
    orf_riboseq_qvalue,
    orf_riboseq_reads,
    orf_upstream_neighbor,
    orf_downstream_neighbor,
    orf_upstream_neighbor_distance,
    orf_downstream_neighbor_distance,
    orf_upstream_neighbor_strand,
    orf_downstream_neighbor_strand,
    orf_upstream_neighbor_length,
    orf_downstream_neighbor_length
  )
VALUES (
    1,
    'YAL066W',
    "ATG",
    1,
    3,
    '+',
    3,
    0.5,
    0.5,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ),
  (
    2,
    'YBR196C-A',
    "ATG",
    1,
    3,
    '+',
    3,
    0.5,
    0.5,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
  );
INSERT INTO go_orfs (go_orfs_id, orf_id)
VALUES (1, 1);
INSERT INTO gene_ontology(
    gene_ontology_table_id,
    go_name,
    go_id,
    go_definition,
    study_count,
    study_ratio,
    population_count,
    population_ratio,
    cluster_id,
    study_orfs_id
  )
VALUES (
    1,
    'GO:0003674',
    'GO:0003674',
    'cellular_component',
    1,
    1,
    1,
    1,
    1,
    1
  );
INSERT INTO coexpression_network (orf_id, cluster_id, degree)
VALUES (1, 1, 1);
INSERT INTO coexpression (
    orf_id,
    coexpressed_orf_id,
    rho,
    pairwise_observations,
    pearson_r,
    spearman_r
  )
VALUES (1, 2, 1, 1, 1, 1);
INSERT INTO coexpression_cluster (
    cluster_id,
    cluster_name,
    cluster_size,
    transient_ratio,
    conserved_ratio,
    nei_ratio,
    transient_count,
    conserved_count,
    nei_count,
    bp_count,
    mf_count,
    cc_count,
    tf_count
  )
VALUES (
    1,
    'cluster_1',
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1
  );
SELECT *
FROM coexpression_network
  INNER JOIN orf on coexpression_network.orf_id = orf.orf_id;