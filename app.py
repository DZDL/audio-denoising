import streamlit
import os
import subprocess
import streamlit as st
import librosa
import librosa.display

import matplotlib
import matplotlib.pyplot as plt
import soundfile as sf

max_length = 120  # seconds audio file

command_inference = 'python3 main.py --mode "prediction" --audio_dir_prediction "input/"  --dir_save_prediction "output/" --audio_output_prediction "input.wav"'


def clean_temp():
    """
    Remove all files in specific paths
    """

    paths_to_remove = ['input/',
                       'output/']

    try:
        for path in paths_to_remove:
            for f in os.listdir(path):
                if not 'README' in f:
                    os.remove(os.path.join(path, f))
    except Exception as e:
        print(e)


if __name__ == '__main__':

    clean_temp()  # Clean temporal files on each upload

    # General description

    st.title("Audio denoising - Speech Enhancement")
    st.text("Check licenses and authors: https://github.com/DZDL/audio-denoising")

    # Upload file
    st.subheader("- Choose an audio file")
    uploaded_file = st.file_uploader("Choose an audio file", type=[
        'wav', 'mp3', 'ogg'])

    if uploaded_file is not None:  # File > 0 bytes

        file_details = {"FileName": uploaded_file.name,
                        "FileType": uploaded_file.type,
                        "FileSize": uploaded_file.size}
        st.write(file_details)

        #######################
        # UPLOADED FILE
        #######################
        if (file_details['FileType'] == 'audio/wav' or
            file_details['FileType'] == 'audio/mp3' or
                file_details['FileType'] == 'audio/ogg'):

            if file_details['FileType'] == 'audio/mp3':
                with open('input/noisy_voice_long_t2.mp3', 'wb') as f:
                    f.write(uploaded_file.getbuffer())

                data, samplerate = sf.read('input/noisy_voice_long_t2.mp3')
                sf.write('input/noisy_voice_long_t2.wav', data, samplerate)

            elif file_details['FileType'] == 'audio/ogg':
                with open('input/noisy_voice_long_t2.ogg', 'wb') as f:
                    f.write(uploaded_file.getbuffer())

                data, samplerate = sf.read('input/noisy_voice_long_t2.ogg')
                sf.write('input/noisy_voice_long_t2.wav', data, samplerate)

            elif file_details['FileType'] == 'audio/wav':
                with open('input/noisy_voice_long_t2.wav', 'wb') as f:
                    f.write(uploaded_file.getbuffer())

            st.subheader("Input audio:")

            # INPUT

            audio_file = open('input/noisy_voice_long_t2.wav', 'rb')
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/wav')

            y, sr = librosa.load('input/noisy_voice_long_t2.wav')

            # Tempo and beat
            tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
            st.write('Estimated tempo: {:.2f} beats per minute'.format(tempo))

            # Waveplot
            fig, ax = plt.subplots(nrows=1, sharex=True, sharey=True)
            fig.set_figheight(4)
            fig.set_figwidth(16)
            librosa.display.waveplot(y, sr=sr)
            ax.set(title='Input audio')
            st.pyplot(fig)

            # Chroma
            # hop_lengsss

            # Inference
            result = os.popen(command_inference).read()
            st.text(result)

            # OUTPUT

            st.subheader("Output audio:")

            audio_file = open('output/input.wav', 'rb')
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/wav')
            y, sr = librosa.load('output/input.wav')

            # Tempo and beat
            tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
            st.write('Estimated tempo: {:.2f} beats per minute'.format(tempo))

            # Waveplot
            fig, ax = plt.subplots(nrows=1, sharex=True, sharey=True)
            fig.set_figheight(4)
            fig.set_figwidth(16)
            librosa.display.waveplot(y, sr=sr)
            ax.set(title='Input audio')
            st.pyplot(fig)

            ###################
            st.subheader("Analysis uncompleted but inference completed.")
            ###################

            # Chroma
            # hop_length = 1024
            # x_1_chroma = librosa.feature.chroma_cqt(y=y, sr=sr,hop_length=hop_length)
            # fig, ax = plt.subplots(nrows=1, sharey=True)
            # fig.set_figheight(12)
            # fig.set_figwidth(12)
            # img = librosa.display.specshow(x_1_chroma, x_axis='time',
            #                             y_axis='chroma',
            #                             hop_length=hop_length, ax=ax)
            # ax.set(title='Chroma extraction')
            # fig.colorbar(img, ax=ax)
            # st.pyplot(fig)
