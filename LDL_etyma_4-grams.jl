# A Computational Model for the Assessment of Mutual Intelligibility Among Closely Related Languages
# data: etyma.tsv 

# get info about your Julia version
#versioninfo()

# load necessary packages
using Pkg
Pkg.add(url="https://github.com/MariaHei/JudiLingMeasures.jl") 
Pkg.add(url="https://github.com/MegamindHenry/JudiLing.jl", rev="pycall_optional") 

# if necessary for RCall, define where R Home directory is located
ENV["R_HOME"] = ""
Pkg.build("RCall")
Pkg.add("RCall")


Pkg.add("CSV")
Pkg.add("DataFrames")

# for reading in semantic matrices
Pkg.add("NPZ")

# update JudiLing (=LDL) package if necessary
Pkg.update("JudiLing")

using JudiLing, CSV, RCall, DataFrames, NPZ

# Load the semantic matrices that were processed in Python: .npy files
S_DUT = npzread(joinpath(@__DIR__, "data_forLDL", "S_DUT_etymamatrix.npy"))
S_ENG = npzread(joinpath(@__DIR__, "data_forLDL", "S_ENG_etymamatrix.npy"))
S_GER = npzread(joinpath(@__DIR__, "data_forLDL", "S_GER_etymamatrix.npy"))

# read in Datasets that were processed in Python
etyma_DUT = DataFrame!(CSV.File(joinpath(@__DIR__, "data_forLDL", "etyma_dutchdata.tsv"), delim="	"));
etyma_GER = DataFrame!(CSV.File(joinpath(@__DIR__, "data_forLDL", "etyma_germandata.tsv"), delim="	"));
etyma_ENG = DataFrame!(CSV.File(joinpath(@__DIR__, "data_forLDL", "etyma_englishdata.tsv"), delim="	"));


# Change the separator within the strings from whitespace to .
# Define a list of columns to process
columns_to_process = [:German_IPA, :Dutch_IPA, :English_IPA, :German_Sound_Classes, :Dutch_Sound_Classes, :English_Sound_Classes]  

# Function to replace spaces with periods in a column if it exists
function replace_spaces_with_periods!(df::DataFrame, col::Symbol)
    if hasproperty(df, col)
        df[!, col] .= replace.(df[!, col], ' ' => '.')
    end
end

# List of DataFrames to process
dataframes_to_process = [etyma_DUT, etyma_GER, etyma_ENG]

# Iterate over the DataFrames
for df in dataframes_to_process
    # Iterate over the columns and replace spaces with periods
    for col in columns_to_process
        replace_spaces_with_periods!(df, col)
    end
end

# Define a function to rename columns for combined cue matrix
function rename_columns_without_prefix!(df::DataFrame, prefix::AbstractString)
    for col in names(df)
        new_name = Symbol(replace(string(col), prefix => ""))
        rename!(df, col => new_name)
    end
end

# Remove language info from column names
rename_columns_without_prefix!(etyma_GER, "German_")
rename_columns_without_prefix!(etyma_DUT, "Dutch_")
rename_columns_without_prefix!(etyma_ENG, "English_")

# create cue matrices for training on individual languages
cue_obj_GER = JudiLing.make_cue_matrix(etyma_GER, grams=4, target_col="Sound_Classes", tokenized=true, sep_token=".",
    keep_sep=true,);
cue_obj_DUT = JudiLing.make_cue_matrix(etyma_DUT, grams=4, target_col="Sound_Classes", tokenized=true, sep_token=".",
    keep_sep=true,);
cue_obj_ENG = JudiLing.make_cue_matrix(etyma_ENG, grams=4, target_col="Sound_Classes", tokenized=true, sep_token=".",
    keep_sep=true,);

# comprehension based on train data for GER
F_GER = JudiLing.make_transform_matrix(cue_obj_GER.C, S_GER);
Shat_GER = cue_obj_GER.C * F_GER;
JudiLing.eval_SC(Shat_GER, S_GER, etyma_GER, :Sound_Classes)
#JudiLing.display_matrix(etyma_german, :Sound_Classes, cue_obj_GER, Shat_GER, :S, nrow=3, ncol=5)

# comprehension based on train data for DUT
F_DUT = JudiLing.make_transform_matrix(cue_obj_DUT.C, S_DUT);
Shat_DUT = cue_obj_DUT.C * F_DUT;
JudiLing.eval_SC(Shat_DUT, S_DUT, etyma_DUT, :Sound_Classes)
#JudiLing.display_matrix(etyma_dutch, :Sound_Classes, cue_obj_DUT, Shat_DUT, :S, nrow=3, ncol=5)

# comprehension based on train data for ENG
F_ENG = JudiLing.make_transform_matrix(cue_obj_ENG.C, S_ENG);
Shat_ENG = cue_obj_ENG.C * F_ENG;
JudiLing.eval_SC(Shat_ENG, S_ENG, etyma_ENG, :Sound_Classes)
#JudiLing.display_matrix(etyma_english, :Sound_Classes, cue_obj_ENG, Shat_ENG, :S, nrow=3, ncol=5)

# Cross-language modelling: testing mutual intelligibility by training on lang1 and testing on lang2

####### comprehension GER to DUT

# Create the C matrix (phonological form)
cue_obj_GER, cue_obj_DUT = JudiLing.make_combined_cue_matrix(
    etyma_GER,
    etyma_DUT,
    grams=4,
    tokenized=true,
    sep_token=".",
    keep_sep=true,
  target_col="Sound_Classes")

F_GER = JudiLing.make_transform_matrix(cue_obj_GER.C, S_GER);
Shat_GERtoDUT = cue_obj_DUT.C * F_GER;

# comprehension accuracy with taking only winner into account
JudiLing.eval_SC(Shat_GERtoDUT, S_DUT, S_GER, etyma_DUT, etyma_GER, :Sound_Classes)

#comprehension accuracy with taking first 5 candidates into account
JudiLing.eval_SC_loose(Shat_GERtoDUT,S_DUT, S_GER, 5, etyma_DUT, etyma_GER, :Sound_Classes)

####### comprehension DUT to GER

# Create the C matrix (phonological form)
cue_obj_DUT, cue_obj_GER = JudiLing.make_combined_cue_matrix(
    etyma_DUT,
    etyma_GER,
    grams=4,
    tokenized=true,
    sep_token=".",
    keep_sep=true,
  target_col="Sound_Classes")

F_DUT = JudiLing.make_transform_matrix(cue_obj_DUT.C, S_DUT);
Shat_DUTtoGER = cue_obj_GER.C * F_DUT;

# comprehension accuracy with taking only winner into account
JudiLing.eval_SC(Shat_DUTtoGER, S_GER, S_DUT, etyma_GER, etyma_DUT, :Sound_Classes)

#comprehension accuracy with taking first 5 candidates into account
JudiLing.eval_SC_loose(Shat_DUTtoGER, S_GER, S_DUT, 5, etyma_GER, etyma_DUT, :Sound_Classes)

####### comprehension GER to ENG

# Create the C matrix (phonological form)
cue_obj_GER, cue_obj_ENG = JudiLing.make_combined_cue_matrix(
    etyma_GER,
    etyma_ENG,
    grams=4,
    tokenized=true,
    sep_token=".",
    keep_sep=true,
  target_col="Sound_Classes")

F_GER = JudiLing.make_transform_matrix(cue_obj_GER.C, S_GER);
Shat_GERtoENG = cue_obj_ENG.C * F_GER;

# comprehension accuracy with taking only winner into account
JudiLing.eval_SC(Shat_GERtoENG, S_ENG, S_GER, etyma_ENG, etyma_GER, :Sound_Classes)

#comprehension accuracy with taking first 5 candidates into account
JudiLing.eval_SC_loose(Shat_GERtoENG,S_ENG, S_GER, 5, etyma_ENG, etyma_GER, :Sound_Classes)

####### comprehension ENG to GER

# Create the C matrix (phonological form)
cue_obj_ENG, cue_obj_GER = JudiLing.make_combined_cue_matrix(
    etyma_ENG,
    etyma_GER,
    grams=4,
    tokenized=true,
    sep_token=".",
    keep_sep=true,
  target_col="Sound_Classes")

F_ENG = JudiLing.make_transform_matrix(cue_obj_ENG.C, S_ENG);
Shat_ENGtoGER = cue_obj_GER.C * F_ENG;

# comprehension accuracy with taking only winner into account
JudiLing.eval_SC(Shat_ENGtoGER, S_GER, S_ENG, etyma_GER, etyma_ENG, :Sound_Classes)

#comprehension accuracy with taking first 5 candidates into account
JudiLing.eval_SC_loose(Shat_ENGtoGER, S_GER, S_ENG, 5, etyma_GER, etyma_ENG, :Sound_Classes)

####### comprehension DUT to ENG

# Create the C matrix (phonological form)
cue_obj_DUT, cue_obj_ENG = JudiLing.make_combined_cue_matrix(
    etyma_DUT,
    etyma_ENG,
    grams=4,
    tokenized=true,
    sep_token=".",
    keep_sep=true,
  target_col="Sound_Classes")

F_DUT = JudiLing.make_transform_matrix(cue_obj_DUT.C, S_DUT);
Shat_DUTtoENG = cue_obj_ENG.C * F_DUT;

# comprehension accuracy with taking only winner into account
JudiLing.eval_SC(Shat_DUTtoENG, S_ENG, S_DUT, etyma_ENG, etyma_DUT, :Sound_Classes)

#comprehension accuracy with taking first 5 candidates into account
JudiLing.eval_SC_loose(Shat_DUTtoENG, S_ENG, S_DUT, 5, etyma_ENG, etyma_DUT, :Sound_Classes)

####### comprehension ENG to DUT

# Create the C matrix (phonological form)
cue_obj_ENG, cue_obj_DUT = JudiLing.make_combined_cue_matrix(
    etyma_ENG,
    etyma_DUT,
    grams=4,
    tokenized=true,
    sep_token=".",
    keep_sep=true,
  target_col="Sound_Classes")

F_ENG = JudiLing.make_transform_matrix(cue_obj_ENG.C, S_ENG);
Shat_ENGtoDUT = cue_obj_DUT.C * F_ENG;

# comprehension accuracy with taking only winner into account
JudiLing.eval_SC(Shat_ENGtoDUT, S_DUT, S_ENG, etyma_DUT, etyma_ENG, :Sound_Classes)

#comprehension accuracy with taking first 5 candidates into account
JudiLing.eval_SC_loose(Shat_ENGtoDUT, S_DUT, S_ENG,5, etyma_DUT, etyma_ENG, :Sound_Classes)
