import boto3
import os

def synthesize_speech(input_text_file, output_audio_file):
    polly = boto3.client('polly')

    # Read the text from file
    with open(input_text_file, 'r') as f:
        text = f.read()

    # Request speech synthesis
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Joanna'
    )

    # Save audio
    with open(output_audio_file, 'wb') as f:
        f.write(response['AudioStream'].read())

    print(f"Audio saved to {output_audio_file}")

def upload_to_s3(file_name, bucket, object_name):
    s3 = boto3.client('s3')
    s3.upload_file(file_name, bucket, object_name)
    print(f"Uploaded {file_name} to s3://{bucket}/{object_name}")

if __name__ == "__main__":
    # Strip whitespace/newlines from secrets if present
    if os.getenv("AWS_ACCESS_KEY_ID"):
        os.environ["AWS_ACCESS_KEY_ID"] = os.getenv("AWS_ACCESS_KEY_ID").strip()
    if os.getenv("AWS_SECRET_ACCESS_KEY"):
        os.environ["AWS_SECRET_ACCESS_KEY"] = os.getenv("AWS_SECRET_ACCESS_KEY").strip()

    # Environment vars
    bucket_name = os.getenv("S3_BUCKET")
    prefix = os.getenv("S3_PREFIX", "polly-audio/")
    output_file = os.getenv("OUTPUT_FILENAME", "speech.mp3")

    synthesize_speech("speech.txt", output_file)
    upload_to_s3(output_file, bucket_name, f"{prefix}{output_file}")
