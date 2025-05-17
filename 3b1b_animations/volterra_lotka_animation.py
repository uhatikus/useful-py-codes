from manimlib import *
import numpy as np
from scipy.integrate import odeint

class VolterraLotkaAnimation(Scene):
    def construct(self):
        # System parameters
        alpha = 0.2
        A = 10       
        B = 27       
        C = 9       
        D = 1      
        F = 8       
        T = 10       
        H = 0.1   
        
        background = Rectangle(
            width=FRAME_WIDTH,
            height=FRAME_HEIGHT,
            fill_opacity=1,
            stroke_width=0
        )
        background.set_fill(
                    color=[
                        "#081b29",  # Deep blue
                        "#0a2436",  # Midnight blue
                        "#081b29"   # Deep blue
                    ],
                    opacity=1
                )
        self.add(background)
        
        # Time array
        t = np.linspace(0, T, int(T/H) + 1)
        
        # Just use one initial condition (first one)
        r0, f0 = 2*A, A
        
        # Create the axes for population graph
        population_axes = Axes(
            x_range=[0, T, 1],
            y_range=[0, 60, 10],
            width=12,
            height=7,
            axis_config={"include_tip": False}
        )
        
        population_labels = VGroup(
            population_axes.get_x_axis_label("t", edge=DOWN, buff=0.2),
            population_axes.get_y_axis_label("Population", edge=UP)
        )
        
        population_title = Text("Predator-Prey Population Dynamics", font_size=30)
        population_title.to_edge(UP)
        
        # Position the axes
        population_group = VGroup(population_axes, population_labels)
        population_group.center()
        
        # Add everything to the scene
        self.add(population_axes, population_labels, population_title)
        
        # Legend
        legend_dots = VGroup()
        legend_texts = VGroup()
        
        rabbit_dot = Dot(color=GREEN)
        fox_dot = Dot(color=RED)
        rabbit_text = Text("Rabbits (r)", font_size=20, color=GREEN)
        fox_text = Text("Foxes (f)", font_size=20, color=RED)
        
        rabbit_text.next_to(rabbit_dot, RIGHT)
        fox_text.next_to(fox_dot, RIGHT)
        
        legend_dots.add(rabbit_dot, fox_dot)
        legend_texts.add(rabbit_text, fox_text)
        
        # legend_group = VGroup()
        # for dot, text in zip(legend_dots, legend_texts):
        #     item = VGroup(dot, text)
        #     item.arrange(RIGHT, buff=0.2)
        #     legend_group.add(item)
        
        # legend_group.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        # legend_group.to_corner(UR)
        
        # self.add(legend_group)
        
        # Initial condition display
        initial_text = Text(f"Initial conditions: r₀={r0}, f₀={f0}", font_size=20)
        initial_text.to_corner(UR)
        self.add(initial_text)
        
        # Solve the system
        def volterra_system(y, t, alpha):
            r, f = y
            
            if r <= 0:
                return [0, -f] 
            
            if f <= 0:
                return [2*r, 0]  
            
            drdt = 2*r - alpha*r*f
            dfdt = -f + alpha*r*f
            
            if r < 2:
                drdt = -alpha*r*f  
            if f < 2:
                dfdt = -f  
            
            return [drdt, dfdt]
        
        # Solve the ODE
        solution = odeint(volterra_system, [r0, f0], t, args=(alpha,), atol=1e-6, rtol=1e-6)
        r, f = solution[:, 0], solution[:, 1]
        
        # Ensure non-negative values
        r[r < 0] = 0
        f[f < 0] = 0
        
        # Create population curves
        rabbit_points = [population_axes.coords_to_point(t_val, r_val) for t_val, r_val in zip(t, r)]
        fox_points = [population_axes.coords_to_point(t_val, f_val) for t_val, f_val in zip(t, f)]
        
        rabbit_line = VMobject(color=GREEN, stroke_width=4)
        fox_line = VMobject(color=RED, stroke_width=4)
        
        rabbit_line.set_points_smoothly(rabbit_points)
        fox_line.set_points_smoothly(fox_points)
        
        # Animate the drawing of the curves
        self.play(
            ShowCreation(rabbit_line),
            ShowCreation(fox_line),
            run_time=4
        )
        
        # Add labels for the lines
        rabbit_label = Text("Rabbits", font_size=20, color=GREEN)
        fox_label = Text("Foxes", font_size=20, color=RED)
        
        # Place labels near the end of the lines
        rabbit_label.next_to(rabbit_line.get_end(), UR, buff=0.2)
        fox_label.next_to(fox_line.get_end(), DR, buff=0.2)
        
        self.play(
            FadeIn(rabbit_label),
            FadeIn(fox_label)
        )
        
        # Status text at the bottom
        final_status = ""
        if r[-1] <= 0.1 and f[-1] <= 0.1:
            final_status = "Both rabbits and foxes are dead"
        elif r[-1] <= 0.1:
            final_status = "Rabbits are dead"
        elif f[-1] <= 0.1:
            final_status = "Foxes are dead"
        else:
            final_status = "Both rabbits and foxes are alive"
            
        status_text = Text(f"Result: {final_status}", font_size=24)
        # status_text.to_edge()
        
        self.play(Write(status_text))
        
        # Pause at the end to see the final result
        self.wait(2)

# Auxiliary function to create and save the animation
# if __name__ == "__main__":
    # Command to render the animation
    # Run with:
    # manimgl manim_volterra_lotka.py VolterraLotkaAnimation -o