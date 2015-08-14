CREATE TABLE irs_sched_a (
	form_id_num VARCHAR(38) REFERENCES irs_8872(form_id_num), 
	sched_a_id VARCHAR(38) PRIMARY KEY, 
	org_name VARCHAR(70), 
	ein VARCHAR(9), 
	contributor_name VARCHAR(50), 
	contributor_address_1 VARCHAR(50), 
	contributor_address_2 VARCHAR(50), 
	contributor_address_city VARCHAR(50), 
	contributor_address_state VARCHAR(50), 
	contributor_address_zip VARCHAR(5), 
	contributor_address_zip_ext VARCHAR(4), 
	contributor_emp VARCHAR(70), 
	contribution_amt DOUBLE PRECISION, 
	contributor_occupation VARCHAR(70), 
	agg_contrib_ytd DOUBLE PRECISION, 
	contribution_date VARCHAR(8), 
	empty_field VARCHAR(2)
);
