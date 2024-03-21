import numpy as np

import argparse


from imp_act import make


def do_nothing_policy(observation):
    return [[0] * len(e) for e in observation["edge_observations"]]


def fail_replace_policy(observation):
    actions = []
    for edge in observation["edge_observations"]:
        edge_action = []
        for segment in edge:
            if segment >= 3:
                edge_action.append(3)
            else:
                edge_action.append(0)
        actions.append(edge_action)
    return actions


def heuristic_policy(observation):
    actions = []
    current_time = observation["time_step"]
    for edge in observation["edge_observations"]:
        edge_actions = []
        for segment in edge:
            if segment >= 5:
                edge_actions.append(4)  # Reconstruction
            elif segment >= 5:
                edge_actions.append(3)  # Major repair
            elif segment >= 2:
                edge_actions.append(2)  # Minor repair
            elif current_time % 2 == 0:
                edge_actions.append(1)  # Inspection
            else:
                edge_actions.append(0)  # Do nothing
        actions.append(edge_actions)
    return actions

def get_policy(policy_name):
    if policy_name == "do_nothing":
        return do_nothing_policy
    elif policy_name == "fail_replace":
        return fail_replace_policy
    elif policy_name == "heuristic":
        return heuristic_policy
    else:
        raise ValueError(f"Unknown policy: {policy_name}")

def main(args):
    env = make(args.env)
    obs = env.reset()
    done = False
    timestep = 0
    total_reward = 0
    total_travel_time_reward = 0
    total_maintenance_reward = 0
    total_normalized_delay = 0
    policy = get_policy(args.policy)
    while not done:
        timestep += 1
        actions = policy(obs)
        obs, reward, done, info = env.step(actions)
        total_reward += reward
        total_travel_time_reward += info["reward_elements"][0]
        total_maintenance_reward += info["reward_elements"][1]

        total_normalized_delay += info["normalized_delay"]

        print(f"timestep: {timestep}")
        print(f"reward: {reward:.2e}")
        print(f"travel_time_reward: {info['reward_elements'][0]:.2e}")
        print(f"maintenance_reward: {info['reward_elements'][1]:.2e}")
        print(f"total travel time: {info['total_travel_time']}")
        print(f"remaining budget: {obs['remaining_budget']:.2e}")
        print(f"remaining budget time: {obs['remaining_budget_years']}")
        print(f"normalized delay: {info['normalized_delay']:.5f}")

        flattended_utilizations = [util for edge_util in obs["edge_traffic_utilization"] for util in edge_util]

        max_util = np.max(flattended_utilizations)
        min_util = np.min(flattended_utilizations)
        avg_util = np.mean(flattended_utilizations)
        std_util = np.std(flattended_utilizations)

        print(f"Utilization: avg: {avg_util:.2f}, std: {std_util:.2f}, max: {max_util:.2f}, min: {min_util:.2f}")
        
        
        if args.print_segment_info:
            for i, observations, beliefs, states, util in zip(
                range(len(obs["edge_observations"])),
                obs["edge_observations"],
                obs["edge_beliefs"],
                info["states"],
                obs["edge_traffic_utilization"],
            ):
                print(f"\nedge: {i}")
                print(f"states:       {states}")
                print(f"observations: {observations}")
                print(f"beliefs:      {[list(np.round(belief,2)) for belief in beliefs]}")
                print(f"utilization:  {util}")

        print("=" * 50)

    print(f"total reward: {total_reward:.3e}")
    print(f"total travel time reward: {total_travel_time_reward:.3e}")
    print(f"total maintenance reward: {total_maintenance_reward:.3e}")
    print(f"average normalized delay: {total_normalized_delay/timestep:.3f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", default="Denmark-v1")
    parser.add_argument("--policy", default="heuristic")
    parser.add_argument("--print-segment-info", "-si", action="store_true")
    args = parser.parse_args()
    main(args)
