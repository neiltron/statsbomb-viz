import matplotlib.pyplot as plt
import matplotlib.patches as patches
import json

def draw_field():
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Set the boundaries of the plot to the size of a soccer field
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 80)
    
    # Set background color
    ax.set_facecolor('black')
    fig.set_facecolor('black')
    
    # Soccer field main boundary
    ax.add_patch(patches.Rectangle((0, 0), 100, 80, edgecolor="white", facecolor="none"))
    
    # Goals
    ax.add_patch(patches.Rectangle((0, 35), 2, 10, edgecolor="yellow", facecolor="yellow"))
    ax.add_patch(patches.Rectangle((98, 35), 2, 10, edgecolor="yellow", facecolor="yellow"))
    
    # 18-yard boxes
    ax.add_patch(patches.Rectangle((0, 18), 18, 44, edgecolor="white", facecolor="none"))
    ax.add_patch(patches.Rectangle((82, 18), 18, 44, edgecolor="white", facecolor="none"))
    
    # 6-yard boxes
    ax.add_patch(patches.Rectangle((0, 30), 6, 20, edgecolor="white", facecolor="none"))
    ax.add_patch(patches.Rectangle((94, 30), 6, 20, edgecolor="white", facecolor="none"))

    return fig, ax

def plot_frame(event, index):
    fig, ax = draw_field()

    # Plotting visible area
    visible_area = event['visible_area']
    ax.add_patch(patches.Polygon([(visible_area[i], visible_area[i + 1]) for i in range(0, len(visible_area), 2)], color="yellow", alpha=0.3))

    # Plotting players
    for entity in event['freeze_frame']:
        color = "blue" if entity['teammate'] else "red"
        if entity['actor']:
            color = "purple"
        ax.scatter(entity['location'][0], entity['location'][1], color=color, s=100)
        if entity['keeper']:
            ax.annotate("GK", (entity['location'][0], entity['location'][1]), color="white", ha="center")

    # Add metadata
    ax.set_title(f"Frame ID: {event['event_uuid']}\nWomen's World Cup 2023: England vs Spain", color="white")

    # Save the frame as an image
    plt.savefig(f"frames/{str(index).zfill(4)}_{event['event_uuid']}.png", facecolor=fig.get_facecolor())

if __name__ == "__main__":
    with open('../data/three-sixty_3906390.json') as file:
        data = json.load(file)

        for index, event in enumerate(data):
            plot_frame(event, index)