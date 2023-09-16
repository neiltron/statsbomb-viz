import matplotlib.pyplot as plt
import matplotlib.patches as patches
import json
import os

#####
##
## this script renders a play by play frames of a match using statsbomb event data.
## this data tends to be player-to-player only except for goals, which has
## freeze-frame data for every player on the pitch at the time of the goal.
##
#####

def plot_pitch():
    """Plot a soccer pitch"""
    fig, ax = plt.subplots(figsize=(12,8))
    ax.set_xlim(0,120)
    ax.set_ylim(0,80)
    # Field and Center elements
    field_border = patches.Rectangle((0,0), 120, 80, color="black", zorder=0)
    centre_line = patches.ConnectionPatch((60,0), (60,80), "data", "data", color="white")
    center_circle = patches.Circle((60,40), 14.6, edgecolor="white", fill=False)
    center_spot = patches.Circle((60,40), 0.8, color="white")

    # Penalty Areas (18-yard boxes)
    penalty_area_left = patches.Rectangle((0, 15.82), 19.8, 48.36, linewidth=2, edgecolor='orange', facecolor='none')
    penalty_area_right = patches.Rectangle((100.2, 15.82), 19.8, 48.36, linewidth=2, edgecolor='orange', facecolor='none')
    
    # Goal Areas (6-yard boxes)
    goal_area_left = patches.Rectangle((0, 29.008), 6.6, 21.984, linewidth=2, edgecolor='yellow', facecolor='none')
    goal_area_right = patches.Rectangle((113.4, 29.008), 6.6, 21.984, linewidth=2, edgecolor='yellow', facecolor='none')

    # Goals - I assume that the goals are also rectangles
    goal_left = patches.Rectangle((0, 35.536), -2, 8.928, linewidth=2, edgecolor='blue', facecolor='blue')
    goal_right = patches.Rectangle((120, 35.536), 2, 8.928, linewidth=2, edgecolor='blue', facecolor='blue')

    ax.add_patch(field_border)
    ax.add_patch(centre_line)
    ax.add_patch(center_circle)
    ax.add_patch(center_spot)
    ax.add_patch(penalty_area_left)
    ax.add_patch(penalty_area_right)
    ax.add_patch(goal_area_left)
    ax.add_patch(goal_area_right)
    ax.add_patch(goal_left)
    ax.add_patch(goal_right)
    
    return fig, ax

def plot_event(event, ax, event_num, team_possession, possession_stats, match):
    """Plot a single event on a soccer pitch"""
    event_type = event['type']['name']

    if event_type == "Pass":
        x_start, y_start = event['location']
        x_end, y_end = event['pass']['end_location']
        pass_outcome = event['pass'].get('outcome', {}).get('name', "Successful")
        pass_recipient = event['pass'].get('recipient', {}).get('name', 'Unknown')

        if pass_outcome == "Successful":
            color = "blue"
        else:
            color = "red"

        ax.annotate("", xy=(x_end, y_end), xytext=(x_start, y_start), arrowprops=dict(arrowstyle="->", color=color))
        ax.text(x_start, y_start, event['player']['name'], color="white", fontsize=8)
        
        # Add recipient text to the plot
        ax.text(x_end, y_end, pass_recipient, color="white", fontsize=8)

        ax.set_title(f"Event {event_num}: {event_type} by {event['player']['name']} to {pass_recipient}", loc='left')

    elif event_type == "Carry":
        x_start, y_start = event['location']
        x_end, y_end = event['carry']['end_location']

        ax.annotate("", xy=(x_end, y_end), xytext=(x_start, y_start), arrowprops=dict(arrowstyle="->", color="yellow"))
        ax.text(x_start, y_start, event['player']['name'], color="white", fontsize=8)
        ax.set_title(f"Event {event_num}: {event_type} by {event['player']['name']}", loc='left')

    elif event_type == "Shot":
        x_start, y_start = event['location']
        x_end, y_end = event['shot']['end_location'][:2]

        freeze_frame_data = event['shot'].get('freeze_frame', [])

        for player_data in freeze_frame_data:
            x_frz, y_frz = player_data['location']
            frz_teammate = player_data['teammate']
            frz_color = 'lightblue' if frz_teammate else 'lightgreen'

            ax.scatter(x_frz, y_frz, color=frz_color)
            # Uncomment this line if you wish to display the player names on the freeze frame.
            ax.text(x_frz, y_frz, player_data['player']['name'], color="white", fontsize=8)

        ax.annotate("", xy=(x_end, y_end), xytext=(x_start, y_start), arrowprops=dict(arrowstyle="->", color="purple"))
        ax.text(x_start, y_start, event['player']['name'], color="white", fontsize=8)
        ax.set_title(f"Event {event_num}: {event_type} by {event['player']['name']}", loc='left')

    elif event_type == "Ball Receipt*":
        x_loc, y_loc = event['location']

        ax.scatter(x_loc, y_loc, color="green")
        ax.text(x_loc, y_loc, event['player']['name'], color="white", fontsize=8)
        ax.set_title(f"Event {event_num}: {event_type} by {event['player']['name']}", loc='left')
      
    elif event_type == "Dribble":
        x_loc, y_loc = event['location']
        dribble_outcome = event['dribble'].get('outcome', {}).get('name')

        ax.scatter(x_loc, y_loc, color="orange")
        ax.text(x_loc, y_loc, event['player']['name'], color="white", fontsize=8)
        ax.set_title(f"Event {event_num}: {event_type} (outcome: {dribble_outcome}) by {event['player']['name']}", loc='left') 

    elif event_type == "Pressure":
        x_loc, y_loc = event['location']

        ax.scatter(x_loc, y_loc, color="pink")
        ax.text(x_loc, y_loc, event['player']['name'], color="white", fontsize=8)
        ax.set_title(f"Event {event_num}: {event_type} by {event['player']['name']}", loc='left') 

    elif event_type == "Duel":
        x_loc, y_loc = event['location']
        duel_type = event['duel']['type']['name']

        if event['duel'].get('outcome', False):
          duel_outcome = event['duel']['outcome']['name']
        else:
          duel_outcome = "Unknown"

        ax.scatter(x_loc, y_loc, color="brown")
        ax.text(x_loc, y_loc, event['player']['name'], color="white", fontsize=8)
        ax.set_title(f"Event {event_num}: {event_type} (type: {duel_type}, outcome: {duel_outcome}) by {event['player']['name']}", loc='left') 

    elif event_type == "Clearance":
        x_loc, y_loc = event['location']
        clearance_body_part = event['clearance']['body_part']['name']
        under_pressure = event.get('under_pressure', False)
        
        color = 'cyan'  # Set color for clearance event

        # Plot the player's location during clearance
        ax.scatter(x_loc, y_loc, color=color)
            
        ax.text(x_loc, y_loc, event['player']['name'], color="white", fontsize=8)

        pressure_text = "under pressure" if under_pressure else "not under pressure" # Add pressure info 

        ax.set_title(f"Event {event_num}: {event_type} (body part: {clearance_body_part}, {pressure_text}) by {event['player']['name']}", loc='left')

    elif event_type == "Foul Committed":
        x_loc, y_loc = event['location']

        if event.get('under_pressure', False):
          foul_card = event['foul_committed'].get('card', {}).get('name', None)
        else:
          foul_card = None
            
        color = 'darkred'  # Set color for foul committed event

        # Plot the player's location during foul
        ax.scatter(x_loc, y_loc, color=color)
            
        ax.text(x_loc, y_loc, event['player']['name'], color="white", fontsize=8)
        
        card_text = f"Card: {foul_card}" if foul_card else "No card"

        ax.set_title(f"Event {event_num}: {event_type} ({card_text}) by {event['player']['name']}", loc='left')

    elif event_type == "Foul Won":
        x_loc, y_loc = event['location']
            
        color = 'silver'  # Set color for foul won event

        # Plot the player's location where he won the foul
        ax.scatter(x_loc, y_loc, color=color)
            
        ax.text(x_loc, y_loc, event['player']['name'], color="white", fontsize=8)

        ax.set_title(f"Event {event_num}: {event_type} by {event['player']['name']}", loc='left')

    elif event_type == "Dribbled Past":
        x_loc, y_loc = event['location']
            
        color = 'lightgreen'  # Set color for dribbled past event

        # Plot the player's location where he was dribbled past
        ax.scatter(x_loc, y_loc, color=color)
            
        ax.text(x_loc, y_loc, event['player']['name'], color="white", fontsize=8)

        ax.set_title(f"Event {event_num}: {event_type} by {event['player']['name']}", loc='left')

    elif event_type == "Half Start":
        ax.set_title(f"Event {event_num}: {event_type} - {event['period']} by {event['team']['name']}", loc='left')

    elif event_type == "Ball Recovery":
        x_loc, y_loc = event['location']
            
        color = 'darkgreen'  # Set color for ball recovery event

        # Plot the player's location where he recovered the ball
        ax.scatter(x_loc, y_loc, color=color)
            
        ax.text(x_loc, y_loc, event['player']['name'], color="white", fontsize=8)

        ax.set_title(f"Event {event_num}: {event_type} by {event['player']['name']}", loc='left')

    elif event_type == "Miscontrol":
        x_loc, y_loc = event['location']
            
        color = 'darkorange'  # Set color for miscontrol event

        # Plot the player's location during miscontrol
        ax.scatter(x_loc, y_loc, color=color)
            
        ax.text(x_loc, y_loc, event['player']['name'], color="white", fontsize=8)

        ax.set_title(f"Event {event_num}: {event_type} by {event['player']['name']}", loc='left')

    elif event_type == "Block":
        x_loc, y_loc = event['location']
            
        color = 'darkviolet'  # Set color for block event

        # Plot the player's location during block
        ax.scatter(x_loc, y_loc, color=color)
            
        ax.text(x_loc, y_loc, event['player']['name'], color="white", fontsize=8)

        ax.set_title(f"Event {event_num}: {event_type} by {event['player']['name']}", loc='left')

    elif event_type == "Interception":
        x_loc, y_loc = event['location']
        interception_outcome = event['interception']['outcome']['name']
            
        color = 'darkblue'  # Set color for interception event

        # Plot the player's location during interception
        ax.scatter(x_loc, y_loc, color=color)
            
        ax.text(x_loc, y_loc, event['player']['name'], color="white", fontsize=8)

        ax.set_title(f"Event {event_num}: {event_type} (outcome: {interception_outcome}) by {event['player']['name']}", loc='left')

    elif event_type == "Goal Keeper":
        x_loc, y_loc = event['location']
        keeper_action = event['goalkeeper']['type']['name']

        color = 'lightblue'  # Set color for goalkeeper event

        # Plot the goalkeeper's location during the action
        ax.scatter(x_loc, y_loc, color=color)
            
        ax.text(x_loc, y_loc, event['player']['name'], color="white", fontsize=8)

        ax.set_title(f"Event {event_num}: {event_type} (action: {keeper_action}) by {event['player']['name']}", loc='left')

    match_info = f'Match: {match}'
    ax.text(60, 90, match_info, color="red", fontsize=12, ha='center')

    total_possession = possession_stats['Barcelona'] + possession_stats['Deportivo Alavés'] + .01
    possesion_percentage_barcelona = (possession_stats['Barcelona'] / total_possession) * 100
    possesion_percentage_deportivo = (possession_stats['Deportivo Alavés'] / total_possession) * 100

    # Display possession percentages
    ax.text(120, 85, 'Possession', color="black", fontsize=8, ha='right')
            
    team_posession_info = f"Barcelona {possesion_percentage_barcelona:.2f}%"
    ax.text(120, 83, team_posession_info, color="blue", fontsize=8, ha='right')
    
    team_posession_info = f"Deportivo Alaves {possesion_percentage_deportivo:.2f}%"
    ax.text(120, 81, team_posession_info, color="red", fontsize=8, ha='right')

    
    # Add Team Possession
    team_posession_info = f'Team possession: {team_possession}'
    ax.text(60, 85, team_posession_info, color="blue", fontsize=12, ha='center')

    ax.set_facecolor("black")
    plt.savefig(f'frame_{str(event_num).zfill(4)}.png')
    plt.clf()

def convert_time_to_seconds(time_str):
    """Converts a timestamp string "HH:MM:SS.xxx" into seconds."""
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)

def main():
    with open('../data/events_15946.json', 'r') as file:
        events = json.load(file)

    if not os.path.exists("event_frames"):
        os.makedirs("event_frames")
    
    os.chdir("event_frames")

    match = "Barcelona vs Deportivo Alavés"
    possession_stats = {'Barcelona': 0, 'Deportivo Alavés': 0}

    # set initial possession info
    previous_possession = events[0]['possession_team']['name']
    previous_timestamp = 0  # Initial timestamp

    for idx, event in enumerate(events):
        if event['type']['name'] != 'Starting XI':
            team_possession = event.get('possession_team', {}).get('name', 'Unknown')

            if team_possession != previous_possession:
              current_timestamp = convert_time_to_seconds(event['timestamp'])
              possession_stats[previous_possession] += (current_timestamp - previous_timestamp)

              previous_possession = team_possession
              previous_timestamp = current_timestamp

            fig, ax = plot_pitch()
            plot_event(event, ax, idx+1, team_possession, possession_stats, match)


    plt.close()

if __name__ == "__main__":
    main()
