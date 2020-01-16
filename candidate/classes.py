class Education:
    allowed_fields = ['education', 'board', 'certificate', 'end', 'institute', 'score', 'score_unit',
                      'specialization', 'start']

    def __init__(self):
        self.is_current = False
