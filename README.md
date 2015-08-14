# o_o poindexter o_o
**A tool for wrangling IRS data on 527s**

Poindexter does the following:
* Downloads and extracts the IRS' bulk Political Organization Filing and Disclosure data file
* Cleans this file of database errors, errant DOS and UNIX line endings (there are both), and other cruft
* Repairs lines broken by unsupported characters in the IRS' database dump
* Logs all the weirdness it encounters and repairs
* Writes the results into a series of CSVs, one for each table described in the IRS data documentation [here](http://forms.irs.gov/app/pod/dataDownload/dataDownload)

Poindexter comes complete with the sql statements necessary to make the corresponding tables in a Postgres database.

To download the bulk data:
`./prep_files.sh`

To generate the flatfiles into a directory called 'csvs' -- which should exist in the working directory -- using default settings:
`./run_this.py & tail -f filemaker.log`

From there, you're on your own; SQL scripts are included in `sql/` that will create tables
in Postgresql one could populate from the flatfiles with a `COPY FROM` command.

Poindexter should log an error when it encounters a row it can't handle.
