use std::fs;
use std::cmp::Ordering;

enum Pair<T> {
    Both(T, T),
    One(T),
    None,
}

fn index_twice<T>(slice: &mut [T], a: usize, b: usize) -> Pair<&mut T> {
    if a == b {
        slice.get_mut(a).map_or(Pair::None, Pair::One)
    } else if a >= slice.len() || b >= slice.len() {
        Pair::None
    } else {
        // Safe because a, b are in bounds and distinct
        unsafe {
            let a_ref = &mut *(slice.get_unchecked_mut(a) as *mut _);
            let b_ref = &mut *(slice.get_unchecked_mut(b) as *mut _);
            Pair::Both(a_ref, b_ref)
        }
    }
}

fn gcd(a: i64, b: i64) -> i64 {
    let mut nums = (a, b);
    while nums.1 != 0 {
        nums = (nums.1, nums.0 % nums.1);
    }
    nums.0
}

fn lcm(a: i64, b: i64) -> i64 {
    a * b / gcd(a, b)
}

#[derive(Clone, Eq, PartialEq)]
struct Moon {
    position: [i64; 3],
    velocity: [i64; 3],
}

fn step_dimension(moons: &mut [Moon], dimension: usize) {
    let mut combo_indicies = Vec::new();
    for i in 0..moons.len() {
        for j in i..moons.len() {
            combo_indicies.push([i, j]);
        }
    }
    for pairs in combo_indicies.iter() {
        if let Pair::Both(a, b) = index_twice(moons, pairs[0], pairs[1]) {
            match a.position[dimension].cmp(&b.position[dimension]) {
                Ordering::Greater => {
                    a.velocity[dimension] -= 1;
                    b.velocity[dimension] += 1;
                },
                Ordering::Less => {
                    a.velocity[dimension] += 1;
                    b.velocity[dimension] -= 1;
                },
                _ => {}
            }
        }
    }

    for moon in moons.iter_mut() {
        moon.position[dimension] += moon.velocity[dimension];
    }
}

fn main() {
    let mut moons: Vec<Moon> = Vec::new();

    let contents = fs::read_to_string("../input.txt").unwrap();
    for line in contents.lines() {
        let mut position = [0, 0, 0];
        for (i, part) in line.split(',').enumerate() {
            position[i] = part.replace(">", "")
                .split('=').nth(1).unwrap()
                .parse::<i64>().unwrap();
        }
        moons.push(Moon {
            position,
            velocity: [0, 0, 0],
        });
    }

    let mut periods = [0, 0, 0];

    for _ in 0..1000 {
        for dimension in 0..periods.len() {
            step_dimension(&mut moons, dimension);
        }
    }

    let energy = moons.iter().
        fold(0, |acc: i64, moon| -> i64 {
            acc + moon.velocity
                .iter()
                .map(|v| v.abs())
                .sum::<i64>()
                * moon.position
                .iter()
                .map(|v| v.abs())
                .sum::<i64>()
        });

    println!("{}", energy);

    for (dimension, period) in periods.iter_mut().enumerate() {
        let mut t: i64 = 0;
        let original = moons.clone();
        loop {
            if t > 0 && moons == original {
                *period = t;
                break;
            }

            step_dimension(&mut moons, dimension);
            t += 1;
        }
    }

    println!("{}", lcm(periods[0], lcm(periods[1], periods[2])));
}
