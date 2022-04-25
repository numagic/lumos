window.BENCHMARK_DATA = {
  "lastUpdate": 1650903486533,
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
      },
      {
        "commit": {
          "author": {
            "email": "yunlong@numagic.io",
            "name": "yunlongxu",
            "username": "yunlongxu-numagic"
          },
          "committer": {
            "email": "92360845+yunlongxu-numagic@users.noreply.github.com",
            "name": "Yunlong Xu",
            "username": "yunlongxu-numagic"
          },
          "distinct": true,
          "id": "a0ba303775ea77488a818330b6c70cf0806b4806",
          "message": "test benchmark: tighten tolerance to 1e-6\n\n- should see an increase in iterations used and perhaps also failure\nrate",
          "timestamp": "2022-04-04T09:49:17+02:00",
          "tree_id": "0efc1e9cd6d377ef6626a0039749cab42a7dfcef",
          "url": "https://github.com/numagic/lumos/commit/a0ba303775ea77488a818330b6c70cf0806b4806"
        },
        "date": 1649059361815,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "num_total",
            "value": 7,
            "unit": "-"
          },
          {
            "name": "failure_pct",
            "value": 72,
            "unit": "%"
          },
          {
            "name": "avg_success_iter",
            "value": 55.857142857142854,
            "unit": "iter"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "yunlong@numagic.io",
            "name": "yunlongxu",
            "username": "yunlongxu-numagic"
          },
          "committer": {
            "email": "92360845+yunlongxu-numagic@users.noreply.github.com",
            "name": "Yunlong Xu",
            "username": "yunlongxu-numagic"
          },
          "distinct": true,
          "id": "8f8c39cc9c75bbb181dbc6bd628bd32f19d2204c",
          "message": "fix benchmark bug and test with tolerance 1e-4\n\n- saw lots of restoration failure with 1e-6 tolerance",
          "timestamp": "2022-04-04T10:32:42+02:00",
          "tree_id": "a6e3f7ccd1941d3aa7efd36504fb389964b6edee",
          "url": "https://github.com/numagic/lumos/commit/8f8c39cc9c75bbb181dbc6bd628bd32f19d2204c"
        },
        "date": 1649061997466,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "num_total",
            "value": 25,
            "unit": "-"
          },
          {
            "name": "failure_pct",
            "value": 12,
            "unit": "%"
          },
          {
            "name": "avg_success_iter",
            "value": 53.95454545454545,
            "unit": "iter"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "yunlong@numagic.io",
            "name": "yunlongxu",
            "username": "yunlongxu-numagic"
          },
          "committer": {
            "email": "92360845+yunlongxu-numagic@users.noreply.github.com",
            "name": "Yunlong Xu",
            "username": "yunlongxu-numagic"
          },
          "distinct": true,
          "id": "7632fddbdd73af7dae0d4c63faccf106d3c5b2fd",
          "message": "experiment: restore original tolerance\n\n- should see benchmark numbers return to original values",
          "timestamp": "2022-04-04T11:02:11+02:00",
          "tree_id": "aa0dad9ffe2333fcf907689bb0b88cfebd6c3cb1",
          "url": "https://github.com/numagic/lumos/commit/7632fddbdd73af7dae0d4c63faccf106d3c5b2fd"
        },
        "date": 1649063475985,
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
          "id": "4f24328bdfd356df7693acfdf80e33cf08667d41",
          "message": "add acitons to publish package on release\n\n- add acitons to publish package on release -- caveat is that pypi version number is still manually defined in setup.py an d release version number manually defined on GitHub UI.\r\n- update README, and colab examples to reflect the latest release",
          "timestamp": "2022-04-05T23:40:48+02:00",
          "tree_id": "d8011792056c2b6b510b8ef8f11db94c87194cd5",
          "url": "https://github.com/numagic/lumos/commit/4f24328bdfd356df7693acfdf80e33cf08667d41"
        },
        "date": 1649195538715,
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
          "id": "971110a00db708891157684427fec0aa2a40e89d",
          "message": "redesign scaling\n\n- redesign scaling to move scaling out of the model implicit call, so that it can be set after model_algebra is compiled/jit\r\n- ScalingConfig is designed in a way similar to BoundConfig.",
          "timestamp": "2022-04-10T16:25:44+02:00",
          "tree_id": "c7ce2dd2c7c30ef838e5c0b6d5dc6900ba79f182",
          "url": "https://github.com/numagic/lumos/commit/971110a00db708891157684427fec0aa2a40e89d"
        },
        "date": 1649601326250,
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
            "value": 48.6,
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
          "id": "bd42884c9fe9a159ec522cf2253ab5d2d5fc7a56",
          "message": "unify stage and global var ops and clean up indexing\n\n- move global var and stage var if/else handling from outside into the\r\ninside of DecVarOperator, to remove the need for separate global and stagevar\r\nconfigs for bounds and scales\r\n- remove legacy methods to construct interval variables with global variables appended.\r\n- remove use of jax.numpy inside DecVarOpertor\r\n- add tests for DecVarOperator for getting indices\r\n- remove the possibility to flatten and unflatten on stage\r\n- make dec var enum creation from kwargs only\r\n- update docstring",
          "timestamp": "2022-04-12T11:19:37+02:00",
          "tree_id": "bf862f23713976d369cd72f9e6db95a4b9153b4a",
          "url": "https://github.com/numagic/lumos/commit/bd42884c9fe9a159ec522cf2253ab5d2d5fc7a56"
        },
        "date": 1649755715553,
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
            "value": 48.6,
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
          "id": "4891cd403edd20b0a80efb0e23e507207263c803",
          "message": "clean up problem sizing info\n\n- rename and remove num_con_interval related attributes\r\n- remove number of constraints per stage info\r\n- remove num_var_interval from ocp\r\n- remove num_var_stage from ocp",
          "timestamp": "2022-04-12T15:24:29+02:00",
          "tree_id": "97b65e5dedda87e0d5c79869438b94a5d030488b",
          "url": "https://github.com/numagic/lumos/commit/4891cd403edd20b0a80efb0e23e507207263c803"
        },
        "date": 1649770350188,
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
            "value": 48.6,
            "unit": "iter"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "yunlong@numagic.io",
            "name": "yunlongxu",
            "username": "yunlongxu-numagic"
          },
          "committer": {
            "email": "92360845+yunlongxu-numagic@users.noreply.github.com",
            "name": "Yunlong Xu",
            "username": "yunlongxu-numagic"
          },
          "distinct": true,
          "id": "d47ddd0888ddb25bb653f39120360ab83b7d92e9",
          "message": "add default params to pacejka model\n\n- the default parameters are no longer loaded from a .tir file, which\nmakes the model no longer dependent on having the .tir file on the path.\n(what makes it even worse in the old code is that it was a hard-coded\npaths!)",
          "timestamp": "2022-04-20T23:02:57+02:00",
          "tree_id": "9834deced09befe60acd42e35bcf847acf036be5",
          "url": "https://github.com/numagic/lumos/commit/d47ddd0888ddb25bb653f39120360ab83b7d92e9"
        },
        "date": 1650489063829,
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
            "value": 48.6,
            "unit": "iter"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "yunlong@numagic.io",
            "name": "yunlongxu",
            "username": "yunlongxu-numagic"
          },
          "committer": {
            "email": "92360845+yunlongxu-numagic@users.noreply.github.com",
            "name": "Yunlong Xu",
            "username": "yunlongxu-numagic"
          },
          "distinct": true,
          "id": "5f4d772d52e362f22dc08bd0654a3f7839bc8a3e",
          "message": "pre-release 0.0.2rc1",
          "timestamp": "2022-04-20T23:35:05+02:00",
          "tree_id": "f7257c3316b4173c0602a2b4a9cfa429316ec8f7",
          "url": "https://github.com/numagic/lumos/commit/5f4d772d52e362f22dc08bd0654a3f7839bc8a3e"
        },
        "date": 1650491125970,
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
            "value": 48.6,
            "unit": "iter"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "yunlong@numagic.io",
            "name": "yunlongxu",
            "username": "yunlongxu-numagic"
          },
          "committer": {
            "email": "92360845+yunlongxu-numagic@users.noreply.github.com",
            "name": "Yunlong Xu",
            "username": "yunlongxu-numagic"
          },
          "distinct": true,
          "id": "17115614e1777be45837932af921f89dea29c5d3",
          "message": "cleanup collocation and add tests\n\n- make it cleaner such that transcription users directly uses a\ncollocation interval of [0, 1], instead of [-1, 1].\n- add tests to ensure collocation continuity and some other properties\nsuch as LGR invertibility are satisfied",
          "timestamp": "2022-04-25T18:05:45+02:00",
          "tree_id": "b8cc6916e8b604277ee93b6d42df4f09db70577b",
          "url": "https://github.com/numagic/lumos/commit/17115614e1777be45837932af921f89dea29c5d3"
        },
        "date": 1650903486029,
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
            "value": 49.2,
            "unit": "iter"
          }
        ]
      }
    ]
  }
}