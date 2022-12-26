from ursina import *
import evolib as ev

creature_shader = Shader(name='creature_shader',
vertex = '''
#version 120
void main() {
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
}
''',
fragment='''
#version 120

#ifdef GL_ES
precision mediump float;
#endif

uniform vec2 position;

void main() {
    // fade out from center of particle;
    float dist = distance(gl_FragCoord.xy, position);

    float fade = 1.0 - dist * 2.0;

    gl_FragColor = vec4(fade, 0.0, 0.0, fade);
}
''', 
geometry='',
)

"""
 vec2 center = vec2(0.5, 0.5);

    float dist = distance(gl_FragCoord.xy, center);

    float fade = 1.0 - dist * 2.0;

    gl_FragColor = vec4(fade, 0.0, 0.0, fade);
"""

class Swarm:
    
    def __init__(self) -> None:
        
        self.swarm = ev.Swarm(
            target_x=0,
            target_y=0,
            inertia_factor=0.5,
            cognitive_factor=0.4,
            social_factor=0.7,
            swarm_group_factor=0.5,
            swarm_target_factor=0.8,
            swarm_random_factor=0.5,
            speed=0.4,
            max_speed=1.0,
            total_creatures=100,
        )

        self.entities = []

        self.swarm.randomize()

        self.elapsed = 0

        for p in self.swarm.get_creatures():
            c = Entity(
                model='quad',
                scale=(0.1,0.1,1),
                texture='swarm',
                position=(p[0], p[1], 0),
                shader=creature_shader,
            )
            c.set_shader_input('position', (p[0], p[1]))
            self.entities.append(c)
    
    def update(self):
        self.elapsed += time.dt
        self.swarm.update(time.dt)
        for i, p in enumerate(self.swarm.get_creatures()):
            self.entities[i].x, self.entities[i].y = p[0], p[1]
            self.entities[i].set_shader_input('position', (p[0], p[1]))
            #self.entities[i].set_shader_input('time', self.elapsed)