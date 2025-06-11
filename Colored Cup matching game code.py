import tkinter as tk
from tkinter import messagebox
import random

# Define colors for the cups
colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink']

# Generate a random order of cups
correct_order = random.sample(colors, len(colors))
shuffled_order = correct_order[:]
random.shuffle(shuffled_order)

class CupMatchingGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cup Matching Game")
        self.attributes("-fullscreen", True)  # Fullscreen mode
        self.spaces = [None] * 7  # Define 7 spaces
        self.drag_data = {'index': None, 'widget': None, 'x': 0, 'y': 0}
        self.correct_order_visible = False  # Track whether correct order is visible

        # Keep the reference to the image
        self.celebration_gif = tk.PhotoImage(file=r"D:\Projects\Anvesha 2024\Colored cups matching game\congrats_gif.gif")
        self.hint_gif = tk.PhotoImage(file=r"D:\Projects\Anvesha 2024\Colored cups matching game\hint_popup_gif.gif")  # Load your hint GIF here

        
        self.create_widgets()

    def create_widgets(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Adjust canvas width and height based on screen size
        canvas_width = screen_width - 200
        canvas_height = 400
        self.canvas = tk.Canvas(self, width=canvas_width, height=canvas_height)
        self.canvas.grid(row=0, column=0, columnspan=7, rowspan=5, padx=50, pady=50)

        # Calculate the spacing to center the cups
        cup_width = 120  # Approximate width of each cup including spacing
        total_cups_width = len(correct_order) * cup_width
        start_x = (canvas_width - total_cups_width) // 2

        # Display the correct order (these won't be draggable)
        # tk.Label(self, text="Correct Order:", font=("Arial", 16)).grid(row=0, column=0, columnspan=7, pady=5)
        # for i, color in enumerate(correct_order):
        #     self.draw_cup(i, 75, color, draggable=False, is_correct_order=True, start_x=start_x)

        # # Display the shuffled order that the player can interact with
        # tk.Label(self, text="Shuffled Order:", font=("Arial", 16)).grid(row=2, column=0, columnspan=7, pady=5)
        # for i, color in enumerate(shuffled_order):
        #     self.draw_cup(i, 275, color, draggable=True, is_correct_order=False, start_x=start_x)

        # Display area for Manhattan distance and correct matches
        self.graphics_canvas = tk.Canvas(self, width=150, height=300)
        self.graphics_canvas.grid(row=0, column=7, rowspan=5, padx=10, pady=10)

        # Manhattan distance label (adjusted placement)
        self.manhattan_label = tk.Label(self, text="Manhattan Distance: N/A", font=("Arial", 18, 'bold'), fg="blue")
        self.manhattan_label.grid(row=6, column=0, columnspan=7, pady=5)

        # Correct matches label, initially hidden (adjusted placement)
        self.correct_matches_label = tk.Label(self, text="", font=("Arial", 18, 'bold'), fg="green")
        self.correct_matches_label.grid(row=7, column=0, columnspan=7, pady=5)

        # Add a button to check the order (adjusted placement)
        check_button = tk.Button(self, text="Check Order", font=("Arial", 16), command=self.check_order)
        check_button.grid(row=8, column=0, columnspan=7, pady=10)

        # Add the new Hint button
        hint_button = tk.Button(self, text="Hint", font=("Arial", 16), command=self.show_hint_popup)
        hint_button.grid(row=9, column=0, columnspan=7, pady=10)

        # Exit button for fullscreen mode (adjusted placement)
        exit_button = tk.Button(self, text="Exit", font=("Arial", 16), command=self.quit_game)
        exit_button.grid(row=10, column=0, columnspan=7, pady=10)
        
        # Add the "Show Correct Order" button
        show_correct_button = tk.Button(self, text="Show Correct Order", font=("Arial", 16), command=self.show_correct_order)
        show_correct_button.grid(row=0, column=0, columnspan=7, pady=10)

        self.correct_order_drawn = []
        # Display the shuffled order that the player can interact with
        tk.Label(self, text="Shuffled Order:", font=("Arial", 16)).grid(row=2, column=0, columnspan=7, pady=5)
        for i, color in enumerate(shuffled_order):
            self.draw_cup(i, 275, color, draggable=True, is_correct_order=False, start_x=start_x)
        
        
    def draw_cup(self, index, y_position, color, draggable, is_correct_order, start_x):
        # Coordinates to draw a smoother cup shape with a rim
        x1, y1 = start_x + index * 120 + 30, y_position
        x2, y2 = x1 + 80, y1 + 80
        x3, y3 = x1 + 20, y1 + 15
        x4, y4 = x2 - 20, y2 - 25

        # Draw the main frustum part of the cup
        cup_frustum = self.canvas.create_polygon(
            x3, y1, x4, y1, x2, y2, x1, y2, fill=color, outline='black', width=2
        )

        # Draw the rim at the bottom of the cup
        rim_height = 7
        cup_bottom = self.canvas.create_oval(
            x1, y2, x2, y2 + rim_height, fill=color, outline='black', width=2
        )

        # Group the frustum and the bottom together for movement
        if not is_correct_order:
            self.spaces[index] = [cup_frustum, cup_bottom]

        # If draggable, add drag event bindings
        if draggable:
            self.canvas.tag_bind(cup_frustum, "<Button-1>", self.on_click)
            self.canvas.tag_bind(cup_frustum, "<B1-Motion>", self.on_drag)
            self.canvas.tag_bind(cup_frustum, "<ButtonRelease-1>", self.on_drop)


    def show_correct_order(self):
        if not self.correct_order_visible:
            screen_width = self.winfo_screenwidth()
            canvas_width = screen_width - 200
            cup_width = 120
            total_cups_width = len(correct_order) * cup_width
            start_x = (canvas_width - total_cups_width) // 2
    
            tk.Label(self, text="Correct Order:", font=("Arial", 16)).grid(row=0, column=0, columnspan=7, pady=5)
            for i, color in enumerate(correct_order):
                self.correct_order_drawn.append(self.draw_cup(i, 75, color, draggable=False, is_correct_order=True, start_x=start_x))
            self.correct_order_visible = True
        else:
            # If the correct order is already visible, hide the cups
            for parts in self.correct_order_drawn:
                for part in parts:
                    self.canvas.delete(part)  # Remove each part of the drawn cup
            self.correct_order_drawn.clear()  # Clear the list
            self.correct_order_visible = False


    def on_click(self, event):
        self.drag_data['index'] = self.get_cup_index(event.widget.find_closest(event.x, event.y)[0])
        self.drag_data['x'] = event.x
        self.drag_data['y'] = event.y
    
        # Bring the selected cup to the front
        if self.drag_data['index'] is not None:
            for part in self.spaces[self.drag_data['index']]:
                self.canvas.tag_raise(part)

    def on_drag(self, event):
        # Calculate movement
        dx = event.x - self.drag_data['x']
        dy = event.y - self.drag_data['y']
        
        # Move both frustum and bottom together
        if self.drag_data['index'] is not None:
            for part in self.spaces[self.drag_data['index']]:
                self.canvas.move(part, dx, dy)
        # Update position data
        self.drag_data['x'] = event.x
        self.drag_data['y'] = event.y
    def on_drop(self, event):
        drop_index = self.get_closest_index(event.x, event.y)
        original_index = self.drag_data['index']
    
        if original_index is not None and drop_index is not None and original_index != drop_index:
            # Get bounding boxes of the dragged cup and the target cup
            dragged_cup_bbox = self.canvas.bbox(self.spaces[original_index][0])
            target_cup_bbox = self.canvas.bbox(self.spaces[drop_index][0])
    
            # Calculate the area of both cups
            dragged_cup_area = (dragged_cup_bbox[2] - dragged_cup_bbox[0]) * (dragged_cup_bbox[3] - dragged_cup_bbox[1])
            target_cup_area = (target_cup_bbox[2] - target_cup_bbox[0]) * (target_cup_bbox[3] - target_cup_bbox[1])
    
            # Calculate overlap rectangle
            overlap_x1 = max(dragged_cup_bbox[0], target_cup_bbox[0])
            overlap_y1 = max(dragged_cup_bbox[1], target_cup_bbox[1])
            overlap_x2 = min(dragged_cup_bbox[2], target_cup_bbox[2])
            overlap_y2 = min(dragged_cup_bbox[3], target_cup_bbox[3])
    
            # Calculate overlap area
            overlap_width = max(0, overlap_x2 - overlap_x1)
            overlap_height = max(0, overlap_y2 - overlap_y1)
            overlap_area = overlap_width * overlap_height
    
            # Check if overlap is at least 50% of the dragged cup area
            if overlap_area >= 0.5 * dragged_cup_area:
                # Swap the cup parts (frustum and base) between the two spaces
                self.spaces[original_index], self.spaces[drop_index] = self.spaces[drop_index], self.spaces[original_index]
    
                # Reposition both cups after swapping
                self.update_cup_positions(original_index)
                self.update_cup_positions(drop_index)
            else:
                # If not enough overlap, snap back
                self.update_cup_positions(original_index)
        else:
            # If dropped in the same place, just snap back
            self.update_cup_positions(original_index)
    
        self.drag_data['index'] = None


    def get_cup_index(self, cup_id):
        for index, parts in enumerate(self.spaces):
            if cup_id in parts:
                return index
        return None

    def get_closest_index(self, x, y):
        # Calculate the closest index based on Manhattan distance
        distances = []
        for i, parts in enumerate(self.spaces):
            if parts:
                x1, y1, _, _ = self.canvas.bbox(parts[0])  # Use the frustum for position
                distance = abs(x1 - x) + abs(y1 - y)
                distances.append((distance, i))
        return min(distances, key=lambda t: t[0])[1]

    def update_cup_positions(self, index):
        # Get the starting position for the cups
        screen_width = self.winfo_screenwidth()
        canvas_width = screen_width - 200
        cup_width = 120
        total_cups_width = len(correct_order) * cup_width
        start_x = (canvas_width - total_cups_width) // 2
    
        if self.spaces[index]:
            # Calculate new positions for the frustum and bottom parts of the cup
            new_x1 = start_x + index * cup_width + 30
            new_y1 = 275  # Adjust the Y position for shuffled cups
            x1, y1, _, _ = self.canvas.bbox(self.spaces[index][0])  # Get the current position of the frustum
    
            # Calculate the difference needed to move the cup smoothly
            dx = new_x1 - x1
            dy = new_y1 - y1
    
            # Move both the frustum and bottom part of the cup together
            self.canvas.move(self.spaces[index][0], dx, dy)
            self.canvas.move(self.spaces[index][1], dx, dy)
    def check_order(self):
        current_order = [self.canvas.itemcget(parts[0], "fill") for parts in self.spaces]
        manhattan_distance = self.calculate_manhattan_distance()
        correct_matches = self.calculate_correct_matches()

        # Update the Manhattan distance label
        self.manhattan_label.config(text=f"Manhattan Distance: {manhattan_distance}")

        # Update and show the correct matches label only when the button is clicked
        self.correct_matches_label.config(text=f"Correct Matches: {correct_matches}")

        message = f"Manhattan Distance: {manhattan_distance}\nCorrect Matches: {correct_matches}"

        if current_order == correct_order:
            message += "\n\nCongratulations! You matched the order correctly."
            self.show_celebration_popup(message)
        else:
            message += "\n\nThe order is incorrect. Try again!"
            messagebox.showerror("Result", message)
        
    def show_hint_popup(self):
        hint_window = tk.Toplevel(self)
        hint_window.title("Hint")
    
        # Load the hint GIF for display
        hint_gif = tk.PhotoImage(file=r"E:\Projects\Anvesha 2024\Colored cups matching game\hint_popup_gif.gif")  # Ensure the path is correct
    
        # Check for correctly matched cups and store their colors
        correct_matches = []
        matched_indices = []
        for i, parts in enumerate(self.spaces):
            if parts:
                color = self.canvas.itemcget(parts[0], "fill")
                if color == correct_order[i]:
                    correct_matches.append(color)
                    matched_indices.append(i)
    
        # Check if all cups are matched correctly
        if len(correct_matches) == len(correct_order):
            # Display the hint GIF if all cups are matched
            hint_label = tk.Label(hint_window, image=hint_gif)
            hint_label.image = hint_gif  # Keep a reference to avoid garbage collection
            hint_label.pack(pady=20)
        else:
            # Set cup dimensions and spacing
            cup_width = 80
            cup_spacing = 20
            cup_height = 80  # Height of each cup
            rim_height = 7   # Height of the rim
    
            # Calculate the required canvas width based on the number of cups
            num_cups = len(correct_matches)
            canvas_width = num_cups * (cup_width + cup_spacing) + cup_spacing  # Extra space for margin
            canvas_height = cup_height + rim_height + 20  # Extra space for padding
    
            # Create a canvas in the popup window with a dynamic width and height
            hint_canvas = tk.Canvas(hint_window, width=canvas_width, height=canvas_height)
            hint_canvas.pack(pady=20)
    
            start_x = cup_spacing  # Starting x position for the first cup
    
            # Draw the matched cups on the hint canvas
            for i, index in enumerate(matched_indices):
                color = correct_matches[i]
    
                # Coordinates for the cup in the hint canvas
                x1 = start_x + i * (cup_width + cup_spacing)
                y1 = 20  # Vertical position for drawing the cups (20px from top)
                x2 = x1 + cup_width
                y2 = y1 + cup_height
    
                # Draw the frustum part of the cup in the hint canvas
                hint_canvas.create_polygon(
                    x1 + 20, y1, x1 + cup_width - 20, y1, x2, y2, x1, y2, fill=color, outline='black', width=2
                )
    
                # Draw the rim at the bottom of the cup in the hint canvas
                hint_canvas.create_oval(
                    x1, y2, x2, y2 + rim_height, fill=color, outline='black', width=2
                )
    
        # If no correct matches, show a message
        if not correct_matches:
            no_match_label = tk.Label(hint_window, text="No cups are correctly matched yet!", font=("Arial", 14))
            no_match_label.pack(pady=10)
    
        # Close the hint window after a few seconds
        hint_window.after(3000, hint_window.destroy)  # Auto-close after 3 seconds

    def show_celebration_popup(self, message):
        messagebox.showinfo("Result", message)
        self.show_celebration_gif()

    def show_celebration_gif(self):
        # Create a new window to display the GIF in fullscreen
        gif_window = tk.Toplevel(self)
        gif_window.title("Celebration!")
        
        # Set the window to fullscreen
        gif_window.attributes("-fullscreen", True)
    
        # Create a label to display the GIF
        gif_label = tk.Label(gif_window, image=self.celebration_gif)
        gif_label.pack(expand=True)  # Center the GIF in the window
    
        # Close the GIF window and quit the game after 4 seconds
        gif_window.after(4000, self.quit_game)  # Quit the game after 4 seconds


    def calculate_manhattan_distance(self):
        distance = 0
        for i, parts in enumerate(self.spaces):
            if parts:
                color = self.canvas.itemcget(parts[0], "fill")
                correct_index = correct_order.index(color)
                distance += abs(i - correct_index)
        return distance

    def calculate_correct_matches(self):
        matches = 0
        for i, parts in enumerate(self.spaces):
            if parts:
                color = self.canvas.itemcget(parts[0], "fill")
                if color == correct_order[i]:
                    matches += 1
        return matches

    def get_cup_index(self, cup_id):
        
        for i, parts in enumerate(self.spaces):
            if parts and cup_id in parts:
                return i
        return None

    def get_closest_index(self, x, y):
        min_distance = float('inf')
        closest_index = None
        for i, parts in enumerate(self.spaces):
            if parts:
                x1, y1, x2, y2 = self.canvas.bbox(parts[0])
                distance = abs(x - (x1 + x2) / 2) + abs(y - (y1 + y2) / 2)
                if distance < min_distance:
                    min_distance = distance
                    closest_index = i
        return closest_index

    def quit_game(self):
        self.destroy()

# Run the game
if __name__ == "__main__":
    game = CupMatchingGame()
    game.mainloop()