
import time
import os
import argparse

def main():
    # code to process command line arguments
    parser = argparse.ArgumentParser(description='Peptide Search.')
    parser.add_argument('ph_range', help="Specify the ph range (\"acidic\" for 2.5-3.7, \"wide\" for 3-10).", type=str)
    parser.add_argument('sample_range_min', help="Specify which samples to use (min index, included).", type=int)
    parser.add_argument('sample_range_max', help="Specify which samples to use (max index, not included).", type=int)
    
    # For crux
    parser.add_argument('--crux_bin_path', help="Specify the location of crux's bin folder.", type=str, default="../crux-3.2.Darwin.x86_64/bin/")
    
    # For tide-index
    parser.add_argument('--fasta_dir', help="Specify the location and name of fasta file.", type=str, default="../data/swissprot_human_can-iso_20170206.fasta")
    parser.add_argument('--out_ref_index_dir', help="Specify the reference index directory.", type=str, default="../results/ref-index")
    parser.add_argument('--out_index_dir', help="Specify the output index directory.", type=str, default="../results/index_output")
    parser.add_argument('--max_mods', help="Specify the maximum number of modifications.", type=int, default=4)
    parser.add_argument('--mods_spec', help="Specify the modification specifications.", type=str, default="1STY+79.966, 1M+15.995, C+57.021, K+229.162932")
    parser.add_argument('--nterm_peptide_mods_spec', help="Specify the n-terminus modification specifications.", type=str, default="X+229.162932")
    
    # For tide-search
    parser.add_argument('--ms_dir', help="Specify the location of ms2 files.", type=str, default="../data/ms2_data/")
    parser.add_argument('--out_search_dir', help="Specify the output search directory.", type=str, default="../results/")
    
    # For percolator
    parser.add_argument('--fdr', help="Specify the test FDR.", type=float, default=0.01)
    
    args = parser.parse_args()
    
    start_time_global = time.time()
    print("Arguments are loaded...")
    
    # Add crux path
    job_name = "path"
    
    print("\nRunning ", job_name)
    start_mini_time = time.time()
    #path = "../crux-3.2.Darwin.x86_64/bin/"
    os.environ['PATH'] += ':' + args.crux_bin_path
    cmd = "echo $PATH"
    os.system(cmd)
    print(os.system(cmd))
    end_mini_time = time.time()
    print("Finished ", job_name)
    print("Runtime: ", end_mini_time-start_mini_time)
    
    # Run tide-index
    job_name = "tide-index"
    cmd = "crux tide-index " + args.fasta_dir + " " + args.out_ref_index_dir + " " + " --output-dir \"" + args.out_index_dir + "\" --max-mods " + str(args.max_mods) + " --mods-spec \"" + args.mods_spec + "\" --nterm-peptide-mods-spec \"" + args.nterm_peptide_mods_spec +"\""
    print("\nRunning ", job_name)
    print(cmd)
    start_mini_time = time.time()
    os.system(cmd)
    end_mini_time = time.time()
    print("Finished ", job_name)
    print("Runtime: ", end_mini_time-start_mini_time)
    
    
    for idx in range(args.sample_range_min, args.sample_range_max):
        start_sample_time = time.time()
        
        str_idx = str(idx)
        if idx < 10:
            str_idx = "0" + str_idx
            
        if args.ph_range == "acidic" and idx > 72:
            print("\n***Exceeded the limit.")
            break
        if args.ph_range == "wide" and idx > 60:
            print("\n***Exceeded the limit.")
            break  
        
        if args.ph_range == "acidic":
            sample_filename = "ElenaP_20141223_Hela_ctrl-perv-mit_stTiO2_TMT10_IPG25-37_10of15ul_fr" + str_idx
        else: # "wide"
            sample_filename = "ElenaP_20141223_Hela_ctrl-perv-mit_stTiO2_TMT10_IPG3-10_10of15ul_fr" + str_idx
            
        print("\n***Running for sample: ", sample_filename)

        # Run tide-search
        job_name = "tide-search"

        ms2_filename = args.ms_dir + sample_filename + ".ms2"
        out_foldername = args.out_search_dir + "out_" + sample_filename
        
        #ms2_filename = args.ms_dir + "ElenaP_20141223_Hela_ctrl-perv-mit_stTiO2_TMT10_IPG3-10_10of15ul_fr01.ms2"
        #out_foldername = args.out_search_dir + "out_" + "ElenaP_20141223_Hela_ctrl-perv-mit_stTiO2_TMT10_IPG3-10_10of15ul_fr01"
        cmd = "crux tide-search --compute-sp T " + ms2_filename + " " + args.out_ref_index_dir + " " + " --output-dir \"" + out_foldername + "\""
        print("\n\tRunning ", job_name)
        print("\t", cmd)
        start_mini_time = time.time()
        os.system(cmd)
        end_mini_time = time.time()
        print("\tFinished ", job_name)
        print("\tRuntime: ", end_mini_time-start_mini_time)

        # Run sort-by-column
        job_name = "sort-by-column"

        in_filename = out_foldername + "/tide-search.target.txt"
        out_filename = out_foldername + "/tide-search.target.sort.txt"
        cmd = "crux sort-by-column --column-type real --ascending T " + in_filename + " \"xcorr score\" > " + out_filename
        print("\n\tRunning ", job_name)
        print("\t", cmd)
        start_mini_time = time.time()
        os.system(cmd)
        end_mini_time = time.time()
        print("\tFinished ", job_name)
        print("\tRuntime: ", end_mini_time-start_mini_time)

        # Run percolator
        job_name = "percolator"

        cmd = "crux percolator --test-fdr " + str(args.fdr) + " --train-fdr " + str(args.fdr) + " " + in_filename + " --output-dir \"" + out_foldername + "\""
        print("\n\tRunning ", job_name)
        print("\t", cmd)
        start_mini_time = time.time()
        os.system(cmd)
        end_mini_time = time.time()
        print("\tFinished ", job_name)
        print("\tRuntime: ", end_mini_time-start_mini_time)
        
        # Run sort-by-column
        job_name = "sort-by-column"

        in_filename = out_foldername + "/percolator.target.peptides.txt"
        out_filename = out_foldername + "/percolator.target.peptides.sort.txt"
        cmd = "crux sort-by-column --column-type real --ascending T " + in_filename + " \"percolator q-value\" > " + out_filename
        print("\n\tRunning ", job_name)
        print("\t", cmd)
        start_mini_time = time.time()
        os.system(cmd)
        end_mini_time = time.time()
        print("\tFinished ", job_name)
        print("\tRuntime: ", end_mini_time-start_mini_time)
        
        # Run sort-by-column_2
        job_name = "sort-by-column"

        in_filename = out_foldername + "/percolator.target.peptides.txt"
        out_filename = "../results/all_results/" + sample_filename + "_percolator.target.peptides.sort.txt"
        cmd = "crux sort-by-column --column-type real --ascending T " + in_filename + " \"percolator q-value\" > " + out_filename
        print("\n\tRunning ", job_name)
        print("\t", cmd)
        start_mini_time = time.time()
        os.system(cmd)
        end_mini_time = time.time()
        print("\tFinished ", job_name)
        print("\tRuntime: ", end_mini_time-start_mini_time)

        # Run sort-by-column
        job_name = "sort-by-column"

        in_filename = out_foldername + "/percolator.target.psms.txt"
        out_filename = out_foldername + "/percolator.target.psms.sort.txt"
        cmd = "crux sort-by-column --column-type real --ascending T " + in_filename + " \"percolator score\" > " + out_filename
        print("\n\tRunning ", job_name)
        print("\t", cmd)
        start_mini_time = time.time()
        os.system(cmd)
        end_mini_time = time.time()
        print("\tFinished ", job_name)
        print("\tRuntime: ", end_mini_time-start_mini_time)

        # Run sort-by-column_2
        job_name = "sort-by-column"

        in_filename = out_foldername + "/percolator.target.psms.txt"
        out_filename = "../results/all_results/" + sample_filename + "_percolator.target.psms.sort.txt"
        cmd = "crux sort-by-column --column-type real --ascending T " + in_filename + " \"percolator score\" > " + out_filename
        print("\n\tRunning ", job_name)
        print("\t", cmd)
        start_mini_time = time.time()
        os.system(cmd)
        end_mini_time = time.time()
        print("\tFinished ", job_name)
        print("\tRuntime: ", end_mini_time-start_mini_time)

        
        end_sample_time = time.time()
        print("\n\tRuntime of sample: ", end_sample_time-start_sample_time)

    end_time_global = time.time()
    print("\nTotal runtime: ", end_time_global-start_time_global)

    
if __name__ == "__main__":
    main()