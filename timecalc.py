import itertools
from multiprocessing import Pool, cpu_count
from tqdm import tqdm


def is_valid_time(args):
    """
    Check if the given time components form a valid time based on user-defined conditions.

    Parameters:
    - args (tuple): A tuple containing (h, m, s, ms, digit_set, hour_digits, ms_digits)

    Returns:
    - bool: True if the time is valid based on the conditions, False otherwise.
    """
    h, m, s, ms, digit_set, total_digits, hour_digits, ms_digits = args

    # Convert each component to strings with appropriate zero-padding
    time_digits = (
        list(str(h).zfill(hour_digits)) +
        list(str(m).zfill(2)) +
        list(str(s).zfill(2)) +
        list(str(ms).zfill(ms_digits))
    )

    # Convert characters to integers
    time_digits = [int(d) for d in time_digits]

    # Ensure that each digit in time_digits is in digit_set and that no digits repeat
    if all(d in digit_set for d in time_digits) and len(set(time_digits)) == len(time_digits):
        return True
    return False

def compute_valid_times(
    hour_range,
    minute_range,
    second_range,
    millisecond_range,
    digit_set,
    hour_digits=1,
    ms_digits=3
):
    """
    Compute the number of valid times based on the specified ranges and conditions.

    Parameters:
    - hour_range (range): Range of hours to consider.
    - minute_range (range): Range of minutes to consider.
    - second_range (range): Range of seconds to consider.
    - millisecond_range (range): Range of milliseconds to consider.
    - digit_set (set): Set of digits that must be used exactly once.
    - hour_digits (int): Number of digits for the hour component.
    - ms_digits (int): Number of digits for the millisecond component.

    Returns:
    - int: Total number of valid times.
    - int: Total number of possible times within the specified ranges.
    """
    total_possible_times = (
        len(hour_range) *
        len(minute_range) *
        len(second_range) *
        len(millisecond_range)
    )

    # Prepare arguments for parallel processing
    all_times = itertools.product(hour_range, minute_range, second_range, millisecond_range)
    total_digits = hour_digits + 2 + 2 + ms_digits  # h + mm + ss + SSS

    def generate_args():
        for h, m, s, ms in all_times:
            yield (h, m, s, ms, digit_set, total_digits, hour_digits, ms_digits)

    cpu_cores = cpu_count()
    print(f"Using {cpu_cores} CPU cores for parallel processing.")

    valid_times_count = 0

    with Pool(cpu_cores) as pool:
        # Use imap_unordered for better performance with tqdm and set a lower chunksize
        results = pool.imap_unordered(
            is_valid_time,
            generate_args(),
            chunksize=500  # Reduced chunksize to handle memory better
        )

        # Progress bar to track the iteration progress
        with tqdm(total=total_possible_times, desc="Processing") as pbar:
            for is_valid in results:
                if is_valid:
                    valid_times_count += 1
                pbar.update(1)

        # Properly close the pool after completion
        pool.close()
        pool.join()

    return valid_times_count, total_possible_times

if __name__ == '__main__':

    # Define the ranges for each time component
    start_hour = 1  # Minimum hour value (inclusive)
    end_hour = 9    # Maximum hour value (inclusive)
    hour_digits = 1 # Number of digits for the hour component (1 or 2)

    # Define the range of valid hours (you can use hours from 0 to 9)
    hour_range = range(start_hour, end_hour + 1)

    # Define ranges for minutes, seconds, and milliseconds
    minute_range = range(0, 60)       # Minutes from 0 to 59
    second_range = range(0, 60)       # Seconds from 0 to 59
    ms_digits = 3                     # Number of digits for milliseconds
    max_ms_value = 10**ms_digits - 1  # Maximum value for milliseconds (e.g., 999 for 3 digits)
    millisecond_range = range(0, max_ms_value + 1)

    # Define the set of digits that can be used exactly once
    digit_set = set(range(1, 9))  # Allow only digits from this set, example range(0,9) is [1 .. 8]

    # Compute the valid times
    valid_times_count, total_times_count = compute_valid_times(
        hour_range,
        minute_range,
        second_range,
        millisecond_range,
        digit_set,
        hour_digits,
        ms_digits
    )

    # Display the results
    print(f"\nTotal valid times using digits {sorted(digit_set)} exactly once: {valid_times_count}")
    print(f"Total possible times within the specified ranges: {total_times_count}")

    # Calculate and display the probability
    if total_times_count > 0:
        probability = valid_times_count / total_times_count
        print(f"Probability: {probability:.6%}")
    else:
        print("No possible times within the specified ranges.")
