window.BENCHMARK_DATA = {
  "lastUpdate": 1649022143167,
  "repoUrl": "https://github.com/numagic/lumos",
  "entries": {
    "Benchmark": [
      {
        "commit": {
          "author": {
            "name": "numagic",
            "username": "numagic"
          },
          "committer": {
            "name": "numagic",
            "username": "numagic"
          },
          "id": "2dfbb47b9cae0f815f1c8bc0df39a92b794d68cb",
          "message": "add laptime simulation regression test",
          "timestamp": "2022-03-15T14:25:23Z",
          "url": "https://github.com/numagic/lumos/pull/4/commits/2dfbb47b9cae0f815f1c8bc0df39a92b794d68cb"
        },
        "date": 1648764824765,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "num_total",
            "value": 25,
            "unit": "-"
          },
          {
            "name": "failure_pct",
            "value": 0,
            "unit": "%"
          },
          {
            "name": "avg_success_iter",
            "value": 56.2,
            "unit": "iter"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "numagic",
            "username": "numagic"
          },
          "committer": {
            "name": "numagic",
            "username": "numagic"
          },
          "id": "77f99b2c013c5269e7245a4807863d9422ad7575",
          "message": "add laptime simulation regression test",
          "timestamp": "2022-03-15T14:25:23Z",
          "url": "https://github.com/numagic/lumos/pull/4/commits/77f99b2c013c5269e7245a4807863d9422ad7575"
        },
        "date": 1648765686607,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "num_total",
            "value": 25,
            "unit": "-"
          },
          {
            "name": "failure_pct",
            "value": 0,
            "unit": "%"
          },
          {
            "name": "avg_success_iter",
            "value": 56.84,
            "unit": "iter"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "numagic",
            "username": "numagic"
          },
          "committer": {
            "name": "numagic",
            "username": "numagic"
          },
          "id": "93daf28f1f3c997f58777fe25bc468e743073d44",
          "message": "add laptime simulation regression test",
          "timestamp": "2022-03-15T14:25:23Z",
          "url": "https://github.com/numagic/lumos/pull/4/commits/93daf28f1f3c997f58777fe25bc468e743073d44"
        },
        "date": 1648766672539,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "num_total",
            "value": 25,
            "unit": "-"
          },
          {
            "name": "failure_pct",
            "value": 0,
            "unit": "%"
          },
          {
            "name": "avg_success_iter",
            "value": 56.2,
            "unit": "iter"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "92360845+yunlongxu-numagic@users.noreply.github.com",
            "name": "Yunlong Xu",
            "username": "yunlongxu-numagic"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "19bc8dac3f53cbb70a5516190f95d29da1f9bbe5",
          "message": "add laptime simulation regression test\n\n- add a laptime simulation regression test that sweeps all the track, and then record the convergence flat as well as number of iterations, and report it on the GitHub page portal. The portal update is only run for push on main, but the test is run for all PRs, and would fail the PR if an error is thrown.\r\n- in order to run these tests nicely, we modify the FixedMeshOCP to allow changing mesh_scale after creation, the main issue is the cached linear constraint jacobian for continuity can no longer be cached.\r\n- now we can change tracks without reconstructing the ocp, and hence reducing the completing/jitting overhead for backends such as jax.\r\n- also updated bound setting methods to create a default bound setting method and a bound update method.\r\n- update and add tests accordingly.",
          "timestamp": "2022-04-03T23:33:43+02:00",
          "tree_id": "1a508fbe590de3b50185550e5572a049e25bf566",
          "url": "https://github.com/numagic/lumos/commit/19bc8dac3f53cbb70a5516190f95d29da1f9bbe5"
        },
        "date": 1649022142139,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "num_total",
            "value": 25,
            "unit": "-"
          },
          {
            "name": "failure_pct",
            "value": 0,
            "unit": "%"
          },
          {
            "name": "avg_success_iter",
            "value": 50.92,
            "unit": "iter"
          }
        ]
      }
    ]
  }
}