import os
import ffmpeg

def convert_avi_to_mp4(avi_path):
    """Converts an AVI file to MP4 format using FFmpeg."""
    if not os.path.exists(avi_path):
        raise FileNotFoundError(f"File not found: {avi_path}")
    
    mp4_path = avi_path.replace(".avi", ".mp4")
    try:
        (
            ffmpeg
            .input(avi_path)
            .output(mp4_path, vcodec='libx264', acodec='aac')
            .run(overwrite_output=True)
        )
        return mp4_path
    except Exception as e:
        print(f"Video conversion failed: {e}")
        return None

if __name__ == "__main__":
    input_avi = "output.avi"  # Change this to your recorded AVI file path
    converted_mp4 = convert_avi_to_mp4(input_avi)
    
    if converted_mp4:
        print(f"✅ Conversion successful! MP4 file saved at: {converted_mp4}")
    else:
        print("❌ Conversion failed!")

