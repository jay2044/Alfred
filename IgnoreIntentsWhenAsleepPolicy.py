from typing import List, Optional, Dict, Text, Any
from rasa.core.policies.policy import Policy, PolicyPrediction
from rasa.shared.core.trackers import DialogueStateTracker
from rasa.shared.core.domain import Domain
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.core.featurizers.precomputation import MessageContainerForCoreFeaturization
from rasa.shared.core.generator import TrackerWithCachedStates
from rasa.engine.training.fingerprinting import Fingerprintable
from rasa.engine.storage.storage import ModelStorage
from rasa.engine.storage.resource import Resource
from rasa.engine.graph import ExecutionContext

ACTION_LISTEN_NAME = 'action_listen'


@DefaultV1Recipe.register(
    DefaultV1Recipe.ComponentType.POLICY_WITHOUT_END_TO_END_SUPPORT,
    is_trainable=False
)
class IgnoreIntentsWhenAsleepPolicy(Policy):
    def __init__(
            self,
            config: Dict[Text, Any],
            model_storage: Any,
            resource: Any,
            execution_context: Any,
    ):
        super().__init__(config, model_storage, resource, execution_context)

    def predict_action_probabilities(
            self,
            tracker: DialogueStateTracker,
            domain: Domain
    ) -> PolicyPrediction:
        is_asleep = tracker.get_slot('is_asleep')

        # If is_asleep is true, ignore all intents and predict action_listen
        if is_asleep:
            action_name = ACTION_LISTEN_NAME
            confidence = 1.0  # You can set the confidence as needed
            return PolicyPrediction.for_action_name(domain, action_name, self.__class__.__name__, confidence)

        # Default behavior, pass the prediction to the next policy in the pipeline
        probabilities = [0.1, 0.2, 0.7]  # Replace with your computed probabilities
        policy_name = "IgnoreIntentsWhenAsleepPolicy"  # Replace with your policy name if different
        prediction = PolicyPrediction(probabilities, policy_name)
        return prediction

    def persist(self) -> None:
        # Custom policies don't require any persisting
        pass

    @classmethod
    def load(
            cls,
            config: Dict[Text, Any],
            model_storage: ModelStorage,  # Here's the change
            resource: Resource,
            execution_context: ExecutionContext,
    ) -> "IgnoreIntentsWhenAsleepPolicy":
        return cls(config, model_storage, resource, execution_context)

    @staticmethod
    def get_default_config() -> Dict[Text, Any]:
        return {"priority": 1}

    def train(
            self,
            training_trackers: List[TrackerWithCachedStates],
            domain: Domain,
            precomputations: Optional[MessageContainerForCoreFeaturization] = None,
    ) -> Fingerprintable:
        # Your training logic here
        # For example, you can return a dictionary as a fingerprintable output
        fingerprintable_output = {"some_key": "some_value"}

        return fingerprintable_output
