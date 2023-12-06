from autocubing import AutoCubing,create_condition_callable as Found


user_desired_stats = [{'Stat1': 10, 'Stat2': 20}]  # Example stats input by the user  
user_cube_type = 'red'  # Example cube type input by the user

# Now, create the condition callable with the user's input
condition_callable = Found(user_desired_stats, user_cube_type)

# Instantiate the AutoCubing class with the condition_callable
auto_cubing = AutoCubing(condition_callable=condition_callable)

# Start the main process
auto_cubing.main()

