from pydstarlite.implementation import *

def run_both_with_grid(grid, start, goal):
    came_from, cost_so_far = lpa_star_search(grid, start, goal)
    print("########## LPA* ############\n\n\n")
    draw_grid(grid, width=3, point_to=came_from, start=(1, 4), goal=(7, 8))
    print()
    draw_grid(grid, width=3, number=cost_so_far, start=(1, 4), goal=(7, 8))
    print()
    draw_grid(grid, width=3, path=reconstruct_path(came_from, start=(1, 4),
                                                       goal=(7, 8)))
    print("\n\n\n########## A* ############\n\n\n")
    came_from, cost_so_far = a_star_search(grid, start, goal)
    draw_grid(grid, width=3, point_to=came_from, start=(1, 4), goal=(7, 8))
    print()
    draw_grid(grid, width=3, number=cost_so_far, start=(1, 4), goal=(7, 8))
    print()
    draw_grid(grid, width=3, path=reconstruct_path(came_from, start=(1, 4),
                                                       goal=(7, 8)))


if __name__ == "__main__":
    run_both_with_grid(diagram5, (1, 4), (7, 8))