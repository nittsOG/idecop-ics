"""
Attack simulation on the modelled network (A12; D37; docs/03-evaluation-methodology.md §3).

The guide asked for a simulation (D32). This module scores a placement against
a population of simulated attackers. Each one gains initial access at a
foothold and moves to an objective along a loop-free route through the
recorded connections.

The population, fixed before any run (D37):
- footholds: every asset except the Attacker node and the controllers. P's own
  entry assets (Engineering WS, DMZ Jump Host, OT Firewall) are a subset of it.
  Using only those would let any placement that holds them catch every route
  at its first step, which repeats what F's Early term already rewards instead
  of testing it (D37). The documented-entry population is reported as a
  secondary result.
- objectives: every controller (asset type PLC) and every declared path target
  (D33, A36).
- routes: every simple path from a foothold to an objective whose hop count is
  at most the shortest hop count plus a slack s. The primary slack is 1; 0 and
  2 are reported as sensitivity. Connections are walked in either direction,
  as P's own moves are (D33, A35).
- weights: every foothold-objective pair is equally likely, and every route
  within a pair is equally likely.

The expectation over that population is computed exactly, by enumerating
every route. It carries no sampling error and needs no seed: it is the limit
of simulating ever more attackers drawn from the population.

Detection follows what a candidate means (D26): x_l = 1 puts a decoy of
type(l) on l's segment, so a route meets it where the route reaches l. A route
r = (v_1, ..., v_n) is detected at the first position k with v_k in x.
Position 1 is the foothold, where initial access happens, as at P's first
steps. Earliness is (n - k)/(n - 1), the endpoint Early uses (D33): 1 when
caught at the foothold, 0 when caught at the objective.

Not modelled, and stated rather than hidden:
- detectability, an attacker who recognises a decoy and goes round it. F
  prices it with Risk, which is an exposure score and not a probability (D20),
  so it cannot be turned into an avoidance probability without a new
  assumption;
- attacker skill, dwell time and routes through connections the model does
  not record.
No term of F is read here, so the yardstick is not F.
"""
from __future__ import annotations

import networkx as nx

PRIMARY_SLACK = 1
SENSITIVITY_SLACKS = (0, 2)


def controllers(g: nx.DiGraph) -> set[int]:
    """The controllers: asset type PLC (PLC-01, PLC-02 and PLC-03 (RTU) on the testbed)."""
    return {v for v in g if g.nodes[v].get("asset_type") == "PLC"}


def attacker_nodes(g: nx.DiGraph) -> set[int]:
    return {v for v in g if g.nodes[v].get("asset_type") == "Attacker"}


def all_footholds(g: nx.DiGraph) -> list[int]:
    """Primary foothold set: every asset except the Attacker node and the controllers."""
    return sorted(set(g) - attacker_nodes(g) - controllers(g))


def documented_footholds(paths: list[dict]) -> list[int]:
    """Secondary foothold set: the asset of each path's first step."""
    return sorted({p["asset_sequence"][0] for p in paths})


def objectives(g: nx.DiGraph, paths: list[dict]) -> list[int]:
    """Every controller and every declared path target (D33, A36)."""
    return sorted(controllers(g) | {p["target"] for p in paths})


def route_graph(g: nx.DiGraph) -> nx.Graph:
    """The recorded connections without direction, and without the Attacker node."""
    keep = set(g) - attacker_nodes(g)
    u = nx.Graph()
    u.add_nodes_from(sorted(keep))
    u.add_edges_from((a, b) for a, b in g.edges() if a in keep and b in keep)
    return u


def build_population(g: nx.DiGraph, paths: list[dict], slack: int = PRIMARY_SLACK,
                     footholds: list[int] | None = None,
                     targets: list[int] | None = None) -> dict:
    """Every foothold-objective pair with its routes. A pair whose foothold is
    its objective is skipped; an unreachable pair is listed, not dropped silently."""
    if slack < 0:
        raise ValueError("slack must be 0 or more")
    u = route_graph(g)
    fs = all_footholds(g) if footholds is None else sorted(set(footholds))
    ts = objectives(g, paths) if targets is None else sorted(set(targets))
    pairs, unreachable = [], []
    for s in fs:
        for t in ts:
            if s == t:
                continue
            if s not in u or t not in u or not nx.has_path(u, s, t):
                unreachable.append((s, t))
                continue
            d = nx.shortest_path_length(u, s, t)
            routes = sorted(tuple(r) for r in nx.all_simple_paths(u, s, t, cutoff=d + slack))
            pairs.append({"foothold": s, "objective": t, "shortest_hops": d, "routes": routes})
    if not pairs:
        raise ValueError("the population is empty: no foothold reaches an objective")
    return {"slack": slack, "pairs": pairs, "unreachable": unreachable,
            "n_routes": sum(len(p["routes"]) for p in pairs)}


def detection_position(route: tuple[int, ...], x: set[int]) -> int | None:
    """1-based position of the first decoy on the route, or None."""
    for k, v in enumerate(route, start=1):
        if v in x:
            return k
    return None


def evaluate_placement(x: set[int], population: dict) -> dict:
    """Expected detection, detection before the objective, and earliness over
    the population; an undetected route counts 0 in every one."""
    x = set(x)
    pairs = population["pairs"]
    detection = before = earliness = 0.0
    for pair in pairs:
        w = 1.0 / (len(pairs) * len(pair["routes"]))
        for r in pair["routes"]:
            k = detection_position(r, x)
            if k is None:
                continue
            n = len(r)
            detection += w
            if k < n:
                before += w
            earliness += w * (n - k) / (n - 1)
    return {"detection": detection, "before_objective": before, "earliness": earliness}
