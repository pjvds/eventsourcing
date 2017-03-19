from eventsourcing.domain.model.entity import EventSourcedEntity, AbstractEntityRepository, Created
from eventsourcing.domain.model.events import publish, TimestampedVersionEntityEvent
from eventsourcing.exceptions import RepositoryKeyError


class Sequence(EventSourcedEntity):

    class Started(Created):
        """Occurs when sequence is started."""

    class Appended(TimestampedVersionEntityEvent):
        """Occurs when item is appended."""

    @property
    def name(self):
        return self.id


def start_sequence(name):
    event = Sequence.Started(entity_id=name)
    entity = Sequence.mutate(event=event)
    publish(event)
    return entity


class SequenceRepository(AbstractEntityRepository):

    def get_or_create(self, sequence_name):
        """
        Gets or creates a log.

        :rtype: Timebucketedlog
        """
        try:
            return self[sequence_name]
        except RepositoryKeyError:
            return start_sequence(sequence_name)
