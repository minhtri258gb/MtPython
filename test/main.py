import ffmpeg

# # Convert format
# ffmpeg.input("input.mp4").output("output.wmv").run()

# # Extrac sound from video
# ffmpeg.input("input.mp4").output('audio.mp3').run()

# # Cut media
# start_time = '00:00:10' # Start time for trimming (HH:MM:SS)
# end_time = '00:00:20' # End time for trimming (HH:MM:SS)
# ffmpeg.input("input.mp4", ss=start_time, to=end_time).output("trimmed_output.mp4").run()

# # Get image from video
# ffmpeg.input("input.mp4").output('frame_%d.png', vframes=3).run()

# Normal decibel
ffmpeg.input("input.mp3").filter('loudnorm').output("output.mp3")
# ffmpeg -i input.wav -filter:a loudnorm output.wav
# ffmpeg -i origin.mp3 -filter:a loudnorm ffmpeg_cmd.mp3
