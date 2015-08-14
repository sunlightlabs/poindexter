CREATE TABLE irs_related_entities (
	form_id_num VARCHAR(38), 
	entity_id VARCHAR(38), 
	org_name VARCHAR(70), 
	ein VARCHAR(9), 
	entity_name VARCHAR(50), 
	entity_relationship VARCHAR(50), 
	entity_address_1 VARCHAR(50), 
	entity_address_2 VARCHAR(50), 
	entity_address_city VARCHAR(50), 
	entity_address_st VARCHAR(2), 
	entity_address_zip VARCHAR(5), 
	entity_address_zip_ext VARCHAR(4), 
	empty_field VARCHAR(2)
);
