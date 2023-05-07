from ursina import *
import pymunk as pm

class Player(SpriteSheetAnimation):

    def __init__(self, **kwargs):
        super().__init__(
            'hero',
            model='quad',
            tileset_size=(8,6),
            fps=6,
            animations={
                'idle_right' : ((0,5), (3,5)),
                'idle_left' : ((4,5), (7,5)),
                'run_right' : ((0,3), (3,3)),
                'run_left' : ((4,3), (7,3)),
            },
             **kwargs
        )

        self.hand = Sprite(
            shader=kwargs.get('shader'),
            texture='circle',
            color=color.rgb(210, 193, 177),
            parent=self,
            model='quad',
            scale=(0.2,0.2),
            rotation=(0,0,90),
            position=(0.0,-0.1,0),
        )

        self.light = SpotLight(
            position=(20,20,-2),
            color=color.rgb(252, 239, 112),
            shadows=True,
            z=-10,
            y=0,
            x=0
        )
        self.light.look_at(self.hand)
        self.light.add_script(SmoothFollow(
            target=self.hand,
            offset=[0,0,-10],
        ))

        self.selector = Entity(
            model=Quad(mode='line'),
            color=color.black,
            scale=(1,1,1),
            alpha=0.2,
            z=-1
        )

        self.body = pm.Body()      
        self.body.position = kwargs.get('position')
        self.body.velocity = (0,0)
        self.body.velocity_func = self.update_velocity()

        self.shape = pm.Poly.create_box(self.body, size=(0.7,0.7))
        self.shape.mass = 10
        self.shape.elasticity = 0.2
        self.shape.friction = 0.5

        self.speed = 6
        self.dash_speed = 50
        self.is_dashing = False
        self.dash_direction = Vec2(0,0)

        self.current_animation = 'idle_right'

    
    def play_animation(self, animation):
        super().play_animation(animation)
        self.current_animation = animation


    def update(self):
        x, y = self.body.position[0], self.body.position[1] + 0.1
        self.set_position((x, y, 0)) 
        self.update_hand()

        mp = self.hand.world_position
        self.selector.position = mp
        self.selector.x = round(self.selector.x, 0)
        self.selector.y = round(self.selector.y, 0)


    def update_velocity(self):
        def update_v(body, gravity, damping, dt):
            stop_dashing = time.time() - self.is_dashing > 0.05
            velocity = [0,0]
            if self.is_dashing and stop_dashing:
                self.is_dashing = False
            elif self.is_dashing:
                velocity[0] += self.dash_direction.x * self.dash_speed
                velocity[1] += self.dash_direction.y * self.dash_speed
            else:
                if held_keys['a']:
                    velocity[0] -= self.speed
                if held_keys['d']:
                    velocity[0] += self.speed
                if held_keys['w']:
                    velocity[1] += self.speed
                if held_keys['s']:
                    velocity[1] -= self.speed

            body.velocity = velocity

        return update_v


    def update_hand(self):
        mx, my = mouse.x, mouse.y
        px, py = self.screen_position.x, self.screen_position.y
        v = Vec2(mx, my) - Vec2(px, py)
        v.normalize()

        hand_dis = 0.7
        hx, hy = px + (v.x * hand_dis), py + (v.y * hand_dis) - 0.1
        self.hand.x = hx
        self.hand.y = hy

        #self.hand.look_at_2d(Vec3(v.x + self.x, v.y + self.y, 0))


    def input(self, key):
        if key == 'd' or key == 'w':
            self.play_animation('run_right')
        if key == 'a' or key == 's':
            self.play_animation('run_left')
        if key == 'space':
            mx, my = mouse.x, mouse.y
            px, py = self.screen_position.x, self.screen_position.y
            # get the direction from player to the mouse
            v = Vec2(mx, my) - Vec2(px, py)
            v.normalize()
            self.dash_direction = v
            self.is_dashing = time.time()
        
        # if no keys are pressed, play idle animation
        if not held_keys['a'] and not held_keys['d'] and not held_keys['w'] and not held_keys['s']:
            if self.body.velocity[0] > 0:
                self.play_animation('idle_right')
            else:
                self.play_animation('idle_left')
