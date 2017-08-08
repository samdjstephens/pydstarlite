if __name__ == "__main__":
    from pydstarlite.implementation import *
    came_from, cost_so_far = lpa_star_search(diagram4, (2, 4), (2, 9))
    draw_grid(diagram4, width=3, point_to=came_from, start=(2, 4), goal=(2, 9))
    print()
    draw_grid(diagram4, width=3, number=cost_so_far, start=(2, 4), goal=(2, 9))
    print()
    draw_grid(diagram4, width=3, path=reconstruct_path(came_from, start=(2, 4),
                                                       goal=(2, 9)))
    print("\n\n\n########## A* ############\n\n\n")
    came_from, cost_so_far = a_star_search(diagram4, (1, 4), (7, 8))
    draw_grid(diagram4, width=3, point_to=came_from, start=(1, 4), goal=(7, 8))
    print()
    draw_grid(diagram4, width=3, number=cost_so_far, start=(1, 4), goal=(7, 8))
    print()
    draw_grid(diagram4, width=3, path=reconstruct_path(came_from, start=(1, 4),
                                                       goal=(7, 8)))
