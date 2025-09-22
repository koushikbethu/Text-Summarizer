"""
Batch processing script for summarizing multiple files
Useful for processing large numbers of documents
"""

import os
import argparse
from pathlib import Path
from text_summarizer import TextSummarizer
import json
from datetime import datetime

def process_directory(input_dir, output_dir, max_length=150, min_length=30, file_extensions=None):
    """
    Process all files in a directory and save summaries
    
    Args:
        input_dir: Directory containing files to process
        output_dir: Directory to save summaries
        max_length: Maximum summary length
        min_length: Minimum summary length
        file_extensions: List of file extensions to process
    """
    if file_extensions is None:
        file_extensions = ['.pdf', '.txt', '.md']
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize summarizer
    print("Loading AI model...")
    summarizer = TextSummarizer()
    print("✅ Model loaded successfully!")
    
    # Find all files to process
    input_path = Path(input_dir)
    files_to_process = []
    
    for ext in file_extensions:
        files_to_process.extend(input_path.glob(f"**/*{ext}"))
    
    if not files_to_process:
        print(f"No files found with extensions: {file_extensions}")
        return
    
    print(f"Found {len(files_to_process)} files to process")
    
    # Process each file
    results = []
    successful = 0
    failed = 0
    
    for i, file_path in enumerate(files_to_process, 1):
        print(f"\n[{i}/{len(files_to_process)}] Processing: {file_path.name}")
        
        try:
            # Generate summary
            summary = summarizer.process_file(
                str(file_path), 
                max_length=max_length, 
                min_length=min_length
            )
            
            # Create output filename
            output_filename = f"{file_path.stem}_summary.txt"
            output_path = Path(output_dir) / output_filename
            
            # Save summary
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"Summary of: {file_path.name}\n")
                f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Original file: {file_path}\n")
                f.write("-" * 50 + "\n\n")
                f.write(summary)
            
            # Record result
            results.append({
                "file": str(file_path),
                "output": str(output_path),
                "status": "success",
                "summary_length": len(summary)
            })
            
            successful += 1
            print(f"✅ Success: {output_filename}")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            results.append({
                "file": str(file_path),
                "output": None,
                "status": "failed",
                "error": str(e)
            })
            failed += 1
    
    # Save processing report
    report_path = Path(output_dir) / "processing_report.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "total_files": len(files_to_process),
            "successful": successful,
            "failed": failed,
            "results": results
        }, f, indent=2)
    
    print(f"\n🎉 Batch processing completed!")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Report saved to: {report_path}")

def main():
    """Main function for command line usage"""
    parser = argparse.ArgumentParser(description="Batch Text Summarization Tool")
    parser.add_argument("input_dir", help="Directory containing files to process")
    parser.add_argument("output_dir", help="Directory to save summaries")
    parser.add_argument("--max_length", type=int, default=150, help="Maximum summary length")
    parser.add_argument("--min_length", type=int, default=30, help="Minimum summary length")
    parser.add_argument("--extensions", nargs="+", default=['.pdf', '.txt', '.md'], 
                       help="File extensions to process")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_dir):
        print(f"Error: Input directory '{args.input_dir}' does not exist")
        return
    
    process_directory(
        args.input_dir,
        args.output_dir,
        args.max_length,
        args.min_length,
        args.extensions
    )

if __name__ == "__main__":
    main()
