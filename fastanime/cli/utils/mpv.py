import re
import shutil
import subprocess
from typing import Optional

# legacy
# def mpv(link, title: None | str = "anime", *custom_args):
#     MPV = shutil.which("mpv")
#     if not MPV:
#         args = [
#             "nohup",
#             "am",
#             "start",
#             "--user",
#             "0",
#             "-a",
#             "android.intent.action.VIEW",
#             "-d",
#             link,
#             "-n",
#             "is.xyz.mpv/.MPVActivity",
#         ]
#         subprocess.run(args)
#     else:
#         subprocess.run([MPV, *custom_args, f"--title={title}", link])
#


def stream_video(MPV, url, mpv_args, custom_args):
    process = subprocess.Popen(
        [MPV, url, *mpv_args, *custom_args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    last_time = None
    av_time_pattern = re.compile(r"AV: ([0-9:]*) / ([0-9:]*) \(([0-9]*)%\)")
    last_time = "0"
    total_time = "0"

    try:
        while True:
            output = process.stderr.readline()

            if output:
                # Match the timestamp in the output
                match = av_time_pattern.search(output.strip())
                if match:
                    current_time = match.group(1)
                    total_time = match.group(2)
                    match.group(3)
                    last_time = current_time
                    # print(f"Current stream time: {current_time}, Total time: {total_time}, Progress: {percentage}%")

            # Check if the process has terminated
            retcode = process.poll()
            if retcode is not None:
                print("Finshed at: ", last_time)
                break

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        process.terminate()

    return last_time, total_time


def mpv(
    link: str,
    title: Optional[str] = "",
    start_time: str = "0",
    ytdl_format="",
    custom_args=[],
):
    # Determine if mpv is available
    MPV = shutil.which("mpv")

    # If title is None, set a default value

    # Regex to check if the link is a YouTube URL
    youtube_regex = r"(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+"

    if not MPV:
        # Determine if the link is a YouTube URL
        if re.match(youtube_regex, link):
            # Android specific commands to launch mpv with a YouTube URL
            args = [
                "nohup",
                "am",
                "start",
                "--user",
                "0",
                "-a",
                "android.intent.action.VIEW",
                "-d",
                link,
                "-n",
                "com.google.android.youtube/.UrlActivity",
            ]
            return "0", "0"
        else:
            # Android specific commands to launch mpv with a regular URL
            args = [
                "nohup",
                "am",
                "start",
                "--user",
                "0",
                "-a",
                "android.intent.action.VIEW",
                "-d",
                link,
                "-n",
                "is.xyz.mpv/.MPVActivity",
            ]

        subprocess.run(args)
        return "0", "0"
    else:
        # General mpv command with custom arguments
        mpv_args = []
        if start_time != "0":
            mpv_args.append(f"--start={start_time}")
        if title:
            mpv_args.append(f"--title={title}")
        if ytdl_format:
            mpv_args.append(f"--ytdl-format={ytdl_format}")
        stop_time, total_time = stream_video(MPV, link, mpv_args, custom_args)
        return stop_time, total_time


# Example usage
if __name__ == "__main__":
    mpv(
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "Example Video",
        "--fullscreen",
        "--volume=50",
    )
