from manimlib import *
import numpy as np
from scipy.integrate import odeint

class VolterraLotkaAnimation(Scene):
    def construct(self):
        # Set a beautiful background gradient
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
        
        # System parameters
        alpha = 0.1
        A = 10       
        B = 27       
        C = 9       
        D = 1      
        F = 8       
        T = 10       
        H = 0.1   
        
        # Time array
        t = np.linspace(0, T, int(T/H) + 1)
        
        # Define additional initial conditions
        initial_conditions = [
            (2*A, A),       # Standard
            (A, A/2),       # Lower predators
            (A/2, A)        # Lower prey
        ]
        
        # Colors for the curves
        prey_colors = [
            Color("#7DF9FF"),  # Electric blue
            Color("#50C878"),  # Emerald green
            Color("#00FF7F")   # Spring green
        ]
        predator_colors = [
            Color("#FF5E5E"),  # Coral red
            Color("#D70040"),  # Crimson
            Color("#FF2400")   # Scarlet
        ]
        
        # Create the axes for population graph with a nicer look
        population_axes = Axes(
            x_range=[0, T, 1],
            y_range=[0, 60, 10],
            width=12,
            height=7,
            axis_config={
                "include_tip": True, 
                "include_numbers": True,
                "line_to_number_buff": 0.2,
                "stroke_width": 2,
                "stroke_color": WHITE,
                # "number_scale_val": 0.5
            }
        )
        
        # Create better positioned labels with LaTeX styling
        x_label = Tex(r"t \text{ (time)}")
        y_label = Tex(r"\text{Population}")
        
        x_label.next_to(population_axes.x_axis.get_end(), RIGHT + DOWN*0.5)
        y_label.next_to(population_axes.y_axis.get_end(), UP + LEFT*0.5)
        
        # Create grid for better readability
        grid = population_axes.get_grid(n_rows=5, n_cols=6)
        
        # Main title with better styling
        population_title = Text("Volterra-Lotka Predator-Prey Dynamics", font_size=36)
        population_title.set_color_by_gradient([BLUE_A, BLUE_D])
        population_title.to_edge(UP, buff=0.5)
        
        # Position the axes
        population_group = VGroup(population_axes, grid)
        population_group.center()
        
        # Add everything to the scene
        self.add(population_group, x_label, y_label, population_title)
        
        # Add mathematical model explanation
        eq_scale = 0.7
        lotka_volterra_eq = VGroup(
            Tex(r"\frac{dr}{dt} = 2r - \alpha rf", color=prey_colors[0]),
            Tex(r"\frac{df}{dt} = -f + \alpha rf", color=predator_colors[0]),
        )
        lotka_volterra_eq.arrange(DOWN, aligned_edge=LEFT)
        lotka_volterra_eq.scale(eq_scale)
        lotka_volterra_eq.to_corner(DL, buff=0.5)
        
        # Parameter display
        param_text = Tex(r"\alpha = " + str(alpha), font_size=30)
        param_text.next_to(lotka_volterra_eq, DOWN, aligned_edge=LEFT, buff=0.3)
        
        self.play(
            Write(lotka_volterra_eq),
            FadeIn(param_text),
            run_time=2
        )
        
        # Legend with better style
        legend = VGroup()
        
        # We'll add the legend items as we solve each initial condition
        legend_box = Rectangle(
            width=4, 
            height=3, 
            fill_color=BLACK, 
            fill_opacity=0.7,
            stroke_color=WHITE,
            stroke_width=1
        )
        legend_box.to_corner(UR, buff=0.5)
        
        legend_title = Text("Initial Conditions", font_size=20)
        legend_title.set_color(YELLOW)
        legend_title.next_to(legend_box.get_top(), DOWN, buff=0.2)
        
        legend.add(legend_box, legend_title)
        self.add(legend)
        
        # System function for ODE
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
        
        # For tracking the dots along the curves
        trackers = []
        tracker_dots = []
        
        # Solve for each initial condition
        for idx, (r0, f0) in enumerate(initial_conditions):
            # Solve the ODE
            solution = odeint(volterra_system, [r0, f0], t, args=(alpha,), atol=1e-6, rtol=1e-6)
            r, f = solution[:, 0], solution[:, 1]
            
            # Ensure non-negative values
            r[r < 0] = 0
            f[f < 0] = 0
            
            # Create population curves
            rabbit_points = [population_axes.coords_to_point(t_val, r_val) for t_val, r_val in zip(t, r)]
            fox_points = [population_axes.coords_to_point(t_val, f_val) for t_val, f_val in zip(t, f)]
            
            rabbit_line = VMobject(color=prey_colors[idx], stroke_width=3)
            fox_line = VMobject(color=predator_colors[idx], stroke_width=3)
            
            rabbit_line.set_points_smoothly(rabbit_points)
            fox_line.set_points_smoothly(fox_points)
            
            # Add to legend
            legend_item = VGroup()
            
            # Add dots for each curve type
            rabbit_dot = Dot(color=prey_colors[idx])
            fox_dot = Dot(color=predator_colors[idx])
            
            # Labels for legend
            initial_text = Tex(
                f"r_0={r0}, f_0={f0}", 
                font_size=18, 
                color=interpolate_color(prey_colors[idx], predator_colors[idx], 0.5)
            )
            
            # Arrange legend items
            rabbit_label = Text("Rabbits", font_size=16, color=prey_colors[idx])
            fox_label = Text("Foxes", font_size=16, color=predator_colors[idx])
            
            legend_item.add(initial_text)
            legend_item.move_to(legend_box.get_center() + DOWN*(idx-1)*0.5)
            
            legend.add(legend_item)
            
            # Add tracker dots
            rabbit_tracker = Dot(
                color=prey_colors[idx],
                stroke_width=0,
                fill_opacity=0.8,
                radius=0.07
            )
            fox_tracker = Dot(
                color=predator_colors[idx],
                stroke_width=0,
                fill_opacity=0.8,
                radius=0.07
            )
            
            tracker_dots.extend([rabbit_tracker, fox_tracker])
            trackers.append((rabbit_points, fox_points))
            
            # Animate the drawing of the curves
            self.play(
                ShowCreation(rabbit_line),
                ShowCreation(fox_line),
                FadeIn(legend_item),
                run_time=3
            )
        
        # Phase space setup (showing the relationship between prey and predator)
        phase_axes = Axes(
            x_range=[0, 60, 10],
            y_range=[0, 60, 10],
            width=5,
            height=5,
            axis_config={
                "include_tip": True,
                "include_numbers": True,
                "number_scale_val": 0.4
            }
        )
        
        phase_x_label = Tex(r"r \text{ (prey)}")
        phase_y_label = Tex(r"f \text{ (predator)}")
        
        phase_x_label.next_to(phase_axes.x_axis.get_end(), RIGHT + UP*0.1, buff=0.1)
        phase_y_label.next_to(phase_axes.y_axis.get_end(), UP + RIGHT*0.1, buff=0.1)
        
        phase_title = Text("Phase Space", font_size=24)
        phase_title.set_color(YELLOW)
        
        phase_group = VGroup(phase_axes, phase_x_label, phase_y_label, phase_title)
        phase_group.scale(0.7)
        phase_group.to_corner(DR, buff=0.5)
        
        # Add phase grid
        phase_grid = phase_axes.get_grid(stroke_width=0.5, stroke_opacity=0.25)
        phase_group.add_to_back(phase_grid)
        
        self.play(
            FadeIn(phase_group),
            run_time=1
        )
        
        # Create phase space trajectories
        phase_trajectories = []
        
        for idx, ((r0, f0), (rabbit_points, fox_points)) in enumerate(zip(initial_conditions, trackers)):
            # Extract r and f values from points
            r_values = [population_axes.point_to_coords(point)[1] for point in rabbit_points]
            f_values = [population_axes.point_to_coords(point)[1] for point in fox_points]
            
            # Create phase trajectory
            phase_points = [phase_axes.coords_to_point(r, f) for r, f in zip(r_values, f_values)]
            
            phase_traj = VMobject()
            phase_traj.set_points_smoothly(phase_points)
            phase_traj.set_stroke(
                color=interpolate_color(prey_colors[idx], predator_colors[idx], 0.5),
                width=2,
                opacity=0.8
            )
            
            # Add direction arrows along the phase trajectory
            n_arrows = 5
            indices = np.linspace(0, len(phase_points)-2, n_arrows).astype(int)
            
            for i in indices:
                if i+1 < len(phase_points):
                    arrow = Arrow(
                        phase_points[i], 
                        phase_points[i+1],
                        buff=0,
                        stroke_width=2,
                        tip_length=0.1,
                        color=interpolate_color(prey_colors[idx], predator_colors[idx], 0.5)
                    )
                    phase_traj.add(arrow)
            
            phase_trajectories.append(phase_traj)
            
            # Add initial point marker
            init_point = Dot(
                phase_points[0], 
                color=YELLOW, 
                radius=0.05,
                stroke_width=1,
                stroke_color=WHITE
            )
            
            # Label the initial point
            init_label = Tex(f"({r0}, {f0})", font_size=16)
            init_label.next_to(init_point, UR, buff=0.1)
            init_label.scale(0.5)
            
            self.play(
                ShowCreation(phase_traj),
                FadeIn(init_point),
                FadeIn(init_label),
                run_time=2
            )
        
        # Add timeline tracker
        timeline = Line(
            population_axes.coords_to_point(0, 0),
            population_axes.coords_to_point(T, 0),
            color=YELLOW,
            stroke_width=5,
            stroke_opacity=0.5
        )
        
        tracker = Triangle(fill_color=YELLOW, fill_opacity=1, stroke_width=0)
        tracker.scale(0.2)
        tracker.next_to(timeline.get_start(), UP, buff=0)
        
        time_label = Tex("t = 0", color=YELLOW)
        time_label.next_to(tracker, UP, buff=0.3)
        
        self.play(
            FadeIn(timeline),
            FadeIn(tracker),
            FadeIn(time_label),
            run_time=1
        )
        
        # Create all the tracker dots at their starting positions
        for idx, ((r0, f0), (rabbit_points, fox_points)) in enumerate(zip(initial_conditions, trackers)):
            rabbit_tracker = tracker_dots[idx*2]
            fox_tracker = tracker_dots[idx*2 + 1]
            
            rabbit_tracker.move_to(rabbit_points[0])
            fox_tracker.move_to(fox_points[0])
            
            self.add(rabbit_tracker, fox_tracker)
        
        # Animate the movement of all trackers along their paths
        num_steps = len(t)
        step_size = 10  # Skip frames for smoother animation
        
        for i in range(0, num_steps, step_size):
            if i >= len(t):
                break
                
            # Update time tracker
            new_tracker_pos = timeline.get_start() + (timeline.get_end() - timeline.get_start()) * (i / num_steps)
            new_time_value = f"t = {t[i]:.1f}"
            
            # Update all population trackers
            animations = [
                tracker.animate.next_to(new_tracker_pos, UP, buff=0),
                time_label.animate.become(Tex(new_time_value, color=YELLOW).next_to(new_tracker_pos, UP, buff=0.3))
            ]
            
            for idx, (rabbit_points, fox_points) in enumerate(trackers):
                if i < len(rabbit_points) and i < len(fox_points):
                    rabbit_tracker = tracker_dots[idx*2]
                    fox_tracker = tracker_dots[idx*2 + 1]
                    
                    animations.extend([
                        rabbit_tracker.animate.move_to(rabbit_points[i]),
                        fox_tracker.animate.move_to(fox_points[i])
                    ])
            
            self.play(
                *animations,
                run_time=0.1
            )
        
        # Add a conclusion text
        conclusion_text = Text("Dynamics show oscillating population levels with different initial conditions", 
                           font_size=24)
        conclusion_text.set_color_by_gradient([BLUE_A, GREEN_A])
        conclusion_text.to_edge(DOWN, buff=0.5)
        
        self.play(Write(conclusion_text), run_time=2)
        
        # Pause at the end to see the final result
        self.wait(3)

# Auxiliary function to create and save the animation
# if __name__ == "__main__":
    # Command to render the animation
    # Run with:
    # manimgl manim_volterra_lotka.py VolterraLotkaAnimation -o