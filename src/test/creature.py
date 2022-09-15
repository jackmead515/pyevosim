import random
from dataclasses import dataclass
from typing import Tuple, List

import pymunk
import numpy as np

from nn.brain import Brain


def pin_joint(b1, b2, a1=(0,0), a2=(0,0)):
    return pymunk.constraints.PinJoint(b1, b2, a1, a2)


@dataclass
class SegmentAttributes:

    radius: float

    mass: float

    friction: float

    elasticity: float


@dataclass
class CreatureAttributes:

    speed: float

    segment_amount: int

    segment_radius: float

    brain_config: List[Tuple[int, int, str]]


@dataclass
class Segment:

    body: pymunk.Body

    shape: pymunk.Shape

    attr: SegmentAttributes


class Creature:

    def __init__(self, id):
        self.id = id
        self.segments: List[Segment] = []
        self.joints = []
        self.head: Segment = None
        self.attr = CreatureAttributes(
            speed=100,
            segment_amount=5,
            segment_radius=5,
            brain_config=[
                (4, 50, 'relu'),
                (50, 25, 'relu'),
                (25, 5, 'softmax')
            ]
        )
        self.brain = Brain(self.attr.brain_config)


    def initalize(self, position: Tuple[float, float]):
        offset = (self.attr.segment_radius * 2) + 2
        for i in range(self.attr.segment_amount):
            body = pymunk.Body()
            body.position = position[0]+(i*offset), position[1]
            setattr(body, 'id', self.id)

            radius = self.attr.segment_radius+random.random()
            shape = pymunk.Circle(body, radius)
            shape.mass = 0.1
            shape.friction = 1
            shape.elasticity = 0.5

            segment = Segment(
                body=body,
                shape=shape,
                attr=SegmentAttributes(
                    radius=radius,
                    mass=shape.mass,
                    friction=shape.friction,
                    elasticity=shape.elasticity,
                )
            )

            if i == 0:
                self.head = segment

            if len(self.segments):
                joint = pin_joint(self.segments[i-1].body, body)
                self.joints.append(joint)

            self.segments.append(segment)


    def add(self, space):
        for segment in self.segments:
            space.add(segment.body, segment.shape)
        for joint in self.joints:
            space.add(joint)

    
    def decide(self, inputs):
        choice = np.argmax(self.brain.compute(inputs))
        if choice == 0:
            self.apply_force((0, -self.attr.speed))
        elif choice == 1:
            self.apply_force((0, self.attr.speed))
        elif choice == 2:
            self.apply_force((-self.attr.speed, 0))
        elif choice == 3:
            self.apply_force((self.attr.speed, 0))
        elif choice == 4:
            pass


    def apply_force(self, force):
        self.head.body.apply_force_at_local_point(force)