__author__ = 'robin'

from converter import Converter


def test():
    c = Converter()
    info = c.probe('test.mp4')
    c.thumbnail('test.mp4', 10, '/tmp/1.jpg')
    convert = c.convert('test.mp4', '/tmp/output.flv', {
        'format': 'flv',
        'audio': {
            'codec': info.audio.codec,
            'samplerate': info.audio.audio_samplerate,
            'channels': info.audio.audio_channels
        },
        'video': {
            'codec': info.video.codec,
            'width': info.video.video_width,
            'height': info.video.video_height,
            'fps': info.video.video_fps
        }})

    for timecode in convert:
        print "Converting (%f) ...\r" % timecode


if __name__ == '__main__':
    test()
