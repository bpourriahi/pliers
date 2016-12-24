from pliers.converters import Converter
from pliers.converters import get_converter
from pliers.stimuli import Stim
from pliers.stimuli.audio import AudioStim
from pliers.stimuli.video import VideoStim
from pliers.stimuli.text import TextStim


class MultiStepConverter(Converter):
    ''' Base class for Converters doing more than one step.
    Args:
        steps (list): Ordered list describing the sequence of desired
            conversions. Each element in the list can be either a Converter or
            a Stim class. If the former, the exact Converter provided is used
            as the step. If a Stim subclass is passed (e.g., AudioStim), then
            the first matching Converter class will be used.
    '''

    def __init__(self, steps=None):
        super(MultiStepConverter, self).__init__()
        self.steps = self._steps if steps is None else steps

    def _convert(self, stim):
        for i, step in enumerate(self.steps):
            if issubclass(step, Stim):
                converter = get_converter(type(stim), step)
                if converter is None:
                    msg = "Conversion failed at step %d; unable to find a " + \
                            "Converter capable of transforming a %s into a %s." \
                            % (i, stim.__class__.__name__, step.__name__)
                    raise ValueError(msg)
            else:
                converter = step
            stim = converter.transform(stim)                    
        return stim


class VideoToTextConverter(MultiStepConverter):

    _input_type = VideoStim
    _output_type = TextStim
    _steps = [AudioStim, TextStim]