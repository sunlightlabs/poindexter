CREATE TABLE irs_sched_b (
	form_id_num VARCHAR(38) REFERENCES irs_8872(form_id_num), 
	sched_b_id VARCHAR(38) PRIMARY KEY, 
	org_name VARCHAR(70), 
	ein VARCHAR(9), 
	recipient_name VARCHAR(50), 
	recipient_address_1 VARCHAR(50), 
	recipient_address_2 VARCHAR(50), 
	recipient_address_city VARCHAR(50), 
	recipient_address_state VARCHAR(2), 
	recipient_address_zip VARCHAR(5), 
	recipient_address_zip_ext VARCHAR(4), 
	recipient_employer VARCHAR(70), 
	expenditure_amt DOUBLE PRECISION, 
	recipient_occupation VARCHAR(70), 
	expenditure_date VARCHAR(8), 
	expenditure_purpose TEXT, 
	empty_field VARCHAR(2)
);
