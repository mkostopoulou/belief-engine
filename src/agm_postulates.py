from bs import BeliefBase
from contraction_postulates import ContractionPostulates
from revision_postulates import RevisionPostulates

revision_postulates = RevisionPostulates()
contraction_postulates = ContractionPostulates()

class Postulates:
    def __init__(self, engine: BeliefBase) -> None:
        self.engine = engine

    def check_postulate(self, postulate, type):
        if postulate == '1':
            return "Closure is {0}".format('satisfied' if self.closure(type) else 'not satisfied')
        elif postulate == '2':
            return "Success is {0}".format('satisfied' if self.success(type) else 'not satisfied')
        elif postulate == '3':
            return "Inclusion is {0}".format('satisfied' if self.inclusion(type) else 'not satisfied')
        elif postulate == '4':
            return "Vacuity is {0}".format('satisfied' if self.vacuity(type) else 'not satisfied')
        elif postulate == '5':
            if type == 1:
                return "Consistency is {0}".format('satisfied' if revision_postulates.consistency(self.engine) else 'not satisfied')
            else:
                return "Recovery is {0}".format('satisfied' if contraction_postulates.recovery(self.engine) else 'not satisfied')
        elif postulate == '6':
            return "Extensionality is {0}".format('satisfied' if self.extensionality(type) else 'not satisfied')

    def closure(self, type):
        return revision_postulates.closure(self.engine) if type == '1' else contraction_postulates.closure(self.engine)

    def success(self, type):
        return revision_postulates.success(self.engine) if type == '1' else contraction_postulates.success(self.engine)

    def inclusion(self, type):
        return revision_postulates.success(self.engine) if type == '1' else contraction_postulates.success(self.engine)

    def vacuity(self, type):
        return revision_postulates.success(self.engine) if type == '1' else contraction_postulates.success(self.engine)


    def extensionality(self, type):
        return revision_postulates.success(self.engine) if type == '1' else contraction_postulates.success(self.engine)
