from zipfile import ZipFile, ZIP_DEFLATED
import os
from argparse import ArgumentParser
from metadata_stats import REPOS_INFO_METADATA_PATH, JSON_SUFFIX

ZIP_SUFFIX = ".zip"

def main():
    argparser = ArgumentParser(description="Zip metadata files")
    argparser.add_argument("metadata_dir", help="repos_info directory with metadata files")
    argparser.add_argument("--end_date", "-ed", help="End creation date of file to zip (up to, inclusive)", nargs="?", default=None)
    args = argparser.parse_args()

    metadata_dir_list = []
    if args.metadata_dir == "all":
        all_metadata_dir_path = REPOS_INFO_METADATA_PATH
        metadata_dir_list = os.listdir(all_metadata_dir_path)
    else:
        metadata_dir_list.append(args.metadata_dir)

    end_date = args.end_date
    if not end_date:
        print("Please enter an end_date.")
        return 
    
    for metadata_dir in metadata_dir_list: 
        print(f"Zipping all files up to {end_date} for {metadata_dir}")

        metadata_dir_path = REPOS_INFO_METADATA_PATH + metadata_dir + '/'
        metadata_files_list = sorted(os.listdir(metadata_dir_path))

        full_zip_filepath = metadata_dir_path + metadata_dir + "___" + end_date + ZIP_SUFFIX

        with ZipFile(full_zip_filepath, 'w', ZIP_DEFLATED) as zip_obj:
            for filename in metadata_files_list:
                if os.path.splitext(filename)[-1] == ZIP_SUFFIX:
                    continue

                filename_noext = os.path.splitext(filename)[0]
                filename_date = filename_noext[-8:]
                if filename_date > end_date:
                    break

                filename_fullpath = metadata_dir_path + filename
                zip_obj.write(filename_fullpath, arcname=filename)
            
            zipped_filelist = [metadata_dir_path + name for name in zip_obj.namelist()]
            if zipped_filelist:
                for zipped_file in zipped_filelist:
                    os.remove(zipped_file)

if __name__ == "__main__":
    main()