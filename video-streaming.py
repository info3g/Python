
from mpegdash.parser import MPEGDASHParser
import urllib2
import os, xmltodict

class MPEGHelper():

    def __init__(self):
        self.mpd_url = 'http://yt-dash-mse-test.commondatastorage.googleapis.com/media/motion-20120802-manifest.mpd'

    def readMPEGFile(self):
        # mpd = MPEGDASHParser.parse(self.mpd_url)
        # mpd = urllib2.urlopen(self.mpd_url).read()

        data = None
        file_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        file_name = 'TimesNowHD.mpd'
        file_path = os.path.join(file_dir, file_name)
        with open(file_path) as file:
            data = xmltodict.parse(file.read())
            file.close()

        if data:
            data = dict(data)
            if data.has_key('MPD'):
                if isinstance(data['MPD']['Period'], list):
                    periods = data['MPD']['Period']
                    for period in periods:
                        representations = self.getAdaptationSet(period['AdaptationSet'])
                        for representation in representations:
                            representation = dict(representation)
                            time_scale = dict(representation['SegmentTemplate'])['@timescale']
                            segmentTimeline = dict(representation['SegmentTemplate']['SegmentTimeline'])

                            # This is for getting last segments.
                            if isinstance(segmentTimeline['S'], list):
                                segment = dict(segmentTimeline['S'][-1])
                            else:
                                segment = dict(segmentTimeline['S'])
                            
                            # time = segment['@t']
                            duration = segment['@d']
                            time = int(duration) / int(time_scale)
                            print 'time ',time
                            # This is last segment when video was last paused.
                            # here code for start process.
                else:
                    period = dict(data['MPD']['Period'])
                    representations = self.getAdaptationSet(period['AdaptationSet'])
                    for representation in representations:
                        representation = dict(representation)
                        time_scale = dict(representation['SegmentTemplate'])['@timescale']
                        segmentTimeline = dict(representation['SegmentTemplate']['SegmentTimeline'])

                        # This is for getting last segments.
                        if isinstance(segmentTimeline['S'], list):
                            segment = dict(segmentTimeline['S'][-1])
                        else:
                            segment = dict(segmentTimeline['S'])
                        
                        # time = segment['@t']
                        duration = segment['@d']
                        time = int(duration) / int(time_scale)
                        # This is last segment when video was last paused.
                        # here code for start process.
        else:
            print "No data found."

    def getAdaptationSet(self, adaptationSet):
        representations = []
        try:
            for adaptationSet in adaptationSet:
                adaptationSet = dict(adaptationSet)
                content_type = adaptationSet['@contentType']
                if content_type != 'audio':
                    representations = adaptationSet['Representation']
        except:
            representations = []
        return representations

if __name__ == "__main__":
    # objM is an instance for MPEGHelper.
    objM = MPEGHelper()
    objM.readMPEGFile()

    
