window.BENCHMARK_DATA = {
  "lastUpdate": 1662620108675,
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
          "id": "2856250bab35c468596cac7722148ec28f39d14f",
          "message": "improve casadi backend performance\n\n- improve casadi backend performance significnatly for functions that\nare relatively 'light' to run. This is achieved via:\n1) caching the mapped casadi function for the same batch size, as\ncreating the mapped function itself self costs a non-negligible\noverhead.\n2) avoiding turning the casadi sparse matrix into scipy sparse format.",
          "timestamp": "2022-05-09T20:42:34+02:00",
          "tree_id": "db3a6f3fa97a5e170074bbaa73d0f22c7b49f412",
          "url": "https://github.com/numagic/lumos/commit/2856250bab35c468596cac7722148ec28f39d14f"
        },
        "date": 1652122430051,
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
            "value": 48.96,
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
          "id": "c89469703be24940c4d5c818463ec1ae34e4f190",
          "message": "fix boundary condition bug\n\n- fix boundary condition overwritting bug, where updating bounds after\r\nboundary conditions are set will overwrite existing boundary conditions.\r\n- now that boundary conditions will be stored in the problem,, and\r\nappended at every call instead of resetting. The boundary conditions are\r\nthen reapplied everytime when either new boundary conditions are set or\r\nwhen the bounds are updated (updating bounds would otherwise overwrite\r\nboundary conditions already set)\r\n- rename to set_boundary_conditions to update_boundary_conditions to\r\nbe consistent with the bound setting method.\r\n-add corresponding tests",
          "timestamp": "2022-05-10T13:56:31+02:00",
          "tree_id": "d6f0b34f0ba8410a8dfda3f7c874e753df300228",
          "url": "https://github.com/numagic/lumos/commit/c89469703be24940c4d5c818463ec1ae34e4f190"
        },
        "date": 1652184326719,
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
            "value": 47.88,
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
          "id": "55ebcf3819fb9355799506ce70175dda53c607c5",
          "message": "version bump",
          "timestamp": "2022-05-10T14:44:07+02:00",
          "tree_id": "535619386333f1ca2039a7262c0236441e0ac9d4",
          "url": "https://github.com/numagic/lumos/commit/55ebcf3819fb9355799506ce70175dda53c607c5"
        },
        "date": 1652187168862,
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
            "value": 47.88,
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
          "id": "3b54a4caed02842ae2588875989ce512cd60d1bb",
          "message": "Update colab examples",
          "timestamp": "2022-05-11T22:32:20+02:00",
          "tree_id": "8be403388018973fcd48a88450710dabdf08103d",
          "url": "https://github.com/numagic/lumos/commit/3b54a4caed02842ae2588875989ce512cd60d1bb"
        },
        "date": 1652301701646,
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
            "value": 47.88,
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
          "id": "32fc9c9327bc3039acbb60cd389785bf91cdba05",
          "message": "fix bug on creation of summary.json for metrics",
          "timestamp": "2022-05-15T20:46:10+02:00",
          "tree_id": "7e67f6fc22e5d7bdce391ccda970a8941693585f",
          "url": "https://github.com/numagic/lumos/commit/32fc9c9327bc3039acbb60cd389785bf91cdba05"
        },
        "date": 1652641166539,
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
            "value": 47.88,
            "unit": "iter"
          },
          {
            "name": "casadi.100.nlp.objective",
            "value": 0.0002407048999998551,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.gradient",
            "value": 0.000405158199998823,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.constraints",
            "value": 0.007497432100001334,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.jacobian",
            "value": 0.011671996799998396,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.hessian",
            "value": 0.017396502999997666,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.objective",
            "value": 0.000328676699996322,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.gradient",
            "value": 0.0008973682000032567,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.constraints",
            "value": 0.05609391829999595,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.jacobian",
            "value": 0.09881596540000145,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.hessian",
            "value": 0.14399803779999729,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.objective",
            "value": 0.0009661192000066876,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.gradient",
            "value": 0.010608410300005745,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.constraints",
            "value": 0.7262030846000016,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.jacobian",
            "value": 1.2510711519999973,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.hessian",
            "value": 1.697706084699996,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.objective",
            "value": 0.00023643459999220796,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.gradient",
            "value": 0.0003915175999964049,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.constraints",
            "value": 0.004808293499991123,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.jacobian",
            "value": 0.01233821989999342,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.hessian",
            "value": 0.04836565070000916,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.objective",
            "value": 0.00034199690001059937,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.gradient",
            "value": 0.0009471992999920076,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.constraints",
            "value": 0.00978096920000553,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.jacobian",
            "value": 0.10302664879999383,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.hessian",
            "value": 0.46066277420000007,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.objective",
            "value": 0.0009303489000103582,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.gradient",
            "value": 0.00931286900000714,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.constraints",
            "value": 0.05057614670000703,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.jacobian",
            "value": 1.0030395966000014,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.hessian",
            "value": 4.6503105096000015,
            "unit": "sec"
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
          "id": "a559df81f9a4f9bc0c23c04e2629980cf02412df",
          "message": "extract ipopt timing info\n\n- extract nlp and ipopt timing info when the conditions allow it.\n- since these are not parsed by cyipopt, we have to do it the 'hacker'\nway to get it from an output file of ipopt",
          "timestamp": "2022-05-15T21:27:17+02:00",
          "tree_id": "ce2bc99e9c677c8265553018105018af9444bc1c",
          "url": "https://github.com/numagic/lumos/commit/a559df81f9a4f9bc0c23c04e2629980cf02412df"
        },
        "date": 1652643546114,
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
            "value": 47.88,
            "unit": "iter"
          },
          {
            "name": "casadi.100.nlp.objective",
            "value": 0.0002191071999959604,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.gradient",
            "value": 0.00036544529999673616,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.constraints",
            "value": 0.006817502600006265,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.jacobian",
            "value": 0.011011258999997154,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.hessian",
            "value": 0.015482731700001296,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.objective",
            "value": 0.0002900963000001866,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.gradient",
            "value": 0.0008928685999990193,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.constraints",
            "value": 0.04961865910000825,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.jacobian",
            "value": 0.0903973206000046,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.hessian",
            "value": 0.1358869321000043,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.objective",
            "value": 0.0008039996999968935,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.gradient",
            "value": 0.007012700099994618,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.constraints",
            "value": 0.6090756247000059,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.jacobian",
            "value": 1.0734095180000054,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.hessian",
            "value": 1.5499997022999992,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.objective",
            "value": 0.00021091730000080133,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.gradient",
            "value": 0.00035102540000480075,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.constraints",
            "value": 0.00475253839999823,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.jacobian",
            "value": 0.01129880339999545,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.hessian",
            "value": 0.04175220829999944,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.objective",
            "value": 0.0002845962000037616,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.gradient",
            "value": 0.0008424388999969778,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.constraints",
            "value": 0.009536524899999677,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.jacobian",
            "value": 0.08728401719999965,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.hessian",
            "value": 0.35945853369998987,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.objective",
            "value": 0.0008204492000004393,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.gradient",
            "value": 0.007738127499999336,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.constraints",
            "value": 0.04703111040000749,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.jacobian",
            "value": 0.8622251419000009,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.hessian",
            "value": 3.6654547285000034,
            "unit": "sec"
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
          "id": "f3bcf188fdd83f1b2db6d7b1dd5f41cb6440d2f8",
          "message": "version bump",
          "timestamp": "2022-05-15T21:52:38+02:00",
          "tree_id": "e4fbcbc489dff2797aae3e14e620b87736bf8539",
          "url": "https://github.com/numagic/lumos/commit/f3bcf188fdd83f1b2db6d7b1dd5f41cb6440d2f8"
        },
        "date": 1652645332824,
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
            "value": 47.88,
            "unit": "iter"
          },
          {
            "name": "casadi.100.nlp.objective",
            "value": 0.00029709640000419313,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.gradient",
            "value": 0.0005339614999911646,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.constraints",
            "value": 0.010279771700004403,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.jacobian",
            "value": 0.015357291200007239,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.hessian",
            "value": 0.02263334820000864,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.objective",
            "value": 0.0004203290999953424,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.gradient",
            "value": 0.0016560856999944917,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.constraints",
            "value": 0.07420018000000254,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.jacobian",
            "value": 0.12484066189999794,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.hessian",
            "value": 0.17978136660000246,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.objective",
            "value": 0.0010923533999971369,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.gradient",
            "value": 0.013072920299998713,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.constraints",
            "value": 0.8751764811000043,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.jacobian",
            "value": 1.526746773700006,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.hessian",
            "value": 2.0548688590999973,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.objective",
            "value": 0.00029917639999439417,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.gradient",
            "value": 0.00048496040000145513,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.constraints",
            "value": 0.005929267500005153,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.jacobian",
            "value": 0.015498103199990964,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.hessian",
            "value": 0.06331429130000288,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.objective",
            "value": 0.0004057987999999568,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.gradient",
            "value": 0.0011206342000036785,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.constraints",
            "value": 0.012134581599991635,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.jacobian",
            "value": 0.1217700223999941,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.hessian",
            "value": 0.5542172301999926,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.objective",
            "value": 0.0011280642999963674,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.gradient",
            "value": 0.012784645600004297,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.constraints",
            "value": 0.06193443519999846,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.jacobian",
            "value": 1.1652753145000019,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.hessian",
            "value": 5.5412417900000035,
            "unit": "sec"
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
          "id": "fddb48c2f943eca1eafb6b8946cc1c90d9222c11",
          "message": "alwasy remove first call overhead in jitting",
          "timestamp": "2022-05-16T13:48:23+02:00",
          "tree_id": "16f626e379902e1fd190a4a7f77c1b4c768c6266",
          "url": "https://github.com/numagic/lumos/commit/fddb48c2f943eca1eafb6b8946cc1c90d9222c11"
        },
        "date": 1652702564600,
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
            "value": 47.88,
            "unit": "iter"
          },
          {
            "name": "casadi.100.nlp.objective",
            "value": 0.00021436139999195803,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.gradient",
            "value": 0.0003824625999982345,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.constraints",
            "value": 0.007766361999995297,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.jacobian",
            "value": 0.012110420999999861,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.hessian",
            "value": 0.018477163600005043,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.objective",
            "value": 0.0003262220999999954,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.gradient",
            "value": 0.0010228065999967838,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.constraints",
            "value": 0.061919879499998845,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.jacobian",
            "value": 0.10872369160000517,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.hessian",
            "value": 0.15886029509999844,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.objective",
            "value": 0.0009244637999927363,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.gradient",
            "value": 0.0087101463999943,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.constraints",
            "value": 0.7466702653999959,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.jacobian",
            "value": 1.267399258699993,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.hessian",
            "value": 1.7256557639999983,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.objective",
            "value": 0.00024238709999053755,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.gradient",
            "value": 0.0004305571000031705,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.constraints",
            "value": 0.005273658499993417,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.jacobian",
            "value": 0.013175866899996436,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.hessian",
            "value": 0.050099375100000995,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.objective",
            "value": 0.0002982317999908446,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.gradient",
            "value": 0.0009495256000036534,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.constraints",
            "value": 0.009888237899997421,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.jacobian",
            "value": 0.10808183300000565,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.hessian",
            "value": 0.4755570329999955,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.objective",
            "value": 0.000972696399992401,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.gradient",
            "value": 0.009735534100002496,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.constraints",
            "value": 0.05251422889999731,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.jacobian",
            "value": 1.0585776881000015,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.hessian",
            "value": 4.9430420583,
            "unit": "sec"
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
            "email": "92360845+yunlongxu-numagic@users.noreply.github.com",
            "name": "Yunlong Xu",
            "username": "yunlongxu-numagic"
          },
          "distinct": true,
          "id": "af58cb5fbe9dda536448f6e95b8c08f58dbcae95",
          "message": "Update README.md\n\nfix broken links to the colab notebooks",
          "timestamp": "2022-05-17T14:58:53+02:00",
          "tree_id": "40b5997b19ab54e55684683ddca7d3bc253369ec",
          "url": "https://github.com/numagic/lumos/commit/af58cb5fbe9dda536448f6e95b8c08f58dbcae95"
        },
        "date": 1652793128839,
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
            "value": 47.88,
            "unit": "iter"
          },
          {
            "name": "casadi.100.nlp.objective",
            "value": 0.00022996300000386328,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.gradient",
            "value": 0.00045991580000190877,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.constraints",
            "value": 0.007938460599996233,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.jacobian",
            "value": 0.012109313499991003,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.hessian",
            "value": 0.01685408370000232,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.objective",
            "value": 0.0003314842000008866,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.gradient",
            "value": 0.0009535321000043951,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.constraints",
            "value": 0.05515766909999229,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.jacobian",
            "value": 0.09260453379999944,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.hessian",
            "value": 0.13263683870000023,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.objective",
            "value": 0.0009094131999972888,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.gradient",
            "value": 0.010218585600000551,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.constraints",
            "value": 0.6899110995000001,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.jacobian",
            "value": 1.1609742121000068,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.hessian",
            "value": 1.583585526999991,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.objective",
            "value": 0.00019404199999826233,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.gradient",
            "value": 0.0004076141000041389,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.constraints",
            "value": 0.004394624799999747,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.jacobian",
            "value": 0.012002822400006607,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.hessian",
            "value": 0.04596800879999137,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.objective",
            "value": 0.00030339730000150666,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.gradient",
            "value": 0.0009416436999913457,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.constraints",
            "value": 0.009208465799997612,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.jacobian",
            "value": 0.09754717949999758,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.hessian",
            "value": 0.43846729839999626,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.objective",
            "value": 0.000846710799999073,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.gradient",
            "value": 0.00964935389999937,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.constraints",
            "value": 0.04418405709999433,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.jacobian",
            "value": 0.9422800740999946,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.hessian",
            "value": 4.428297746999999,
            "unit": "sec"
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
          "id": "1d9ec5e81f90eb5b363e1ce0f3708225cb2f5134",
          "message": "update colab badges",
          "timestamp": "2022-05-17T15:29:36+02:00",
          "tree_id": "df055cfb3dd3785b889b0da6d608438e2991b0b6",
          "url": "https://github.com/numagic/lumos/commit/1d9ec5e81f90eb5b363e1ce0f3708225cb2f5134"
        },
        "date": 1652795237309,
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
            "value": 48.96,
            "unit": "iter"
          },
          {
            "name": "casadi.100.nlp.objective",
            "value": 0.0003213301000073443,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.gradient",
            "value": 0.0005855502000031265,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.constraints",
            "value": 0.00865239309999879,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.jacobian",
            "value": 0.014000464699995519,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.hessian",
            "value": 0.02243430639999815,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.objective",
            "value": 0.0004296300999953928,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.gradient",
            "value": 0.0012754303999940931,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.constraints",
            "value": 0.06343597789999648,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.jacobian",
            "value": 0.1126237317999994,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.hessian",
            "value": 0.1777248089000068,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.objective",
            "value": 0.0010732303000054344,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.gradient",
            "value": 0.013268654399996648,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.constraints",
            "value": 0.8325502681999979,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.jacobian",
            "value": 1.4380502551000063,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.hessian",
            "value": 2.062568896200003,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.objective",
            "value": 0.00030768999999963853,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.gradient",
            "value": 0.0005607299999951465,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.constraints",
            "value": 0.007056319900004837,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.jacobian",
            "value": 0.017188109900007475,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.hessian",
            "value": 0.06186679940000204,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.objective",
            "value": 0.00040765029999647597,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.gradient",
            "value": 0.0013501110999982302,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.constraints",
            "value": 0.013032671200005553,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.jacobian",
            "value": 0.13307970490000115,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.hessian",
            "value": 0.5905548777000036,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.objective",
            "value": 0.0009816709000006086,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.gradient",
            "value": 0.012081011200007197,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.constraints",
            "value": 0.05937202479999541,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.jacobian",
            "value": 1.2569105116999935,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.hessian",
            "value": 6.130852916400011,
            "unit": "sec"
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
            "email": "92360845+yunlongxu-numagic@users.noreply.github.com",
            "name": "Yunlong Xu",
            "username": "yunlongxu-numagic"
          },
          "distinct": true,
          "id": "68e712f50a85ddcac9a267ece6802b39fec474a0",
          "message": "update brachistochrone example",
          "timestamp": "2022-05-18T17:12:41+02:00",
          "tree_id": "1c66b30e497eff5a3142f87f7d4160ca8092b843",
          "url": "https://github.com/numagic/lumos/commit/68e712f50a85ddcac9a267ece6802b39fec474a0"
        },
        "date": 1652887646720,
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
            "value": 47.88,
            "unit": "iter"
          },
          {
            "name": "casadi.100.nlp.objective",
            "value": 0.00021332279999342063,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.gradient",
            "value": 0.00042852580000953824,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.constraints",
            "value": 0.008514014299998962,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.jacobian",
            "value": 0.012799281900004188,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.hessian",
            "value": 0.019472921500005215,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.objective",
            "value": 0.0003394823999997243,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.gradient",
            "value": 0.0009488968999903591,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.constraints",
            "value": 0.060092184199993424,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.jacobian",
            "value": 0.10473327130000598,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.hessian",
            "value": 0.14928707669999994,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.objective",
            "value": 0.0008601899000041157,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.gradient",
            "value": 0.011920536800005266,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.constraints",
            "value": 0.7941757488000007,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.jacobian",
            "value": 1.3192205444000025,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.hessian",
            "value": 1.8005308634000017,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.objective",
            "value": 0.00021069230000421159,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.gradient",
            "value": 0.00041757459999871573,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.constraints",
            "value": 0.004973365499995453,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.jacobian",
            "value": 0.013438110000004144,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.hessian",
            "value": 0.053764860100000075,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.objective",
            "value": 0.00031176349999668674,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.gradient",
            "value": 0.0009505608000040411,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.constraints",
            "value": 0.010113684999998896,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.jacobian",
            "value": 0.1110148521000042,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.hessian",
            "value": 0.5024398140000017,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.objective",
            "value": 0.0009066708999966977,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.gradient",
            "value": 0.012299216899998555,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.constraints",
            "value": 0.05268105929999365,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.jacobian",
            "value": 1.0901062926999998,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.hessian",
            "value": 5.069546005299992,
            "unit": "sec"
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
          "id": "d9a406c3c9459ec2c3258334238e9d72ec38f3dd",
          "message": "Update readme to include instructions on using Mac-M1 for development",
          "timestamp": "2022-05-25T14:43:36+02:00",
          "tree_id": "44420b0f2f53cd8e89f003d1798648786f9f50e7",
          "url": "https://github.com/numagic/lumos/commit/d9a406c3c9459ec2c3258334238e9d72ec38f3dd"
        },
        "date": 1653483530852,
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
            "value": 47.88,
            "unit": "iter"
          },
          {
            "name": "casadi.100.nlp.objective",
            "value": 0.00025796830000217595,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.gradient",
            "value": 0.0004918458000020109,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.constraints",
            "value": 0.008237994500007062,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.jacobian",
            "value": 0.013621137300003739,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.hessian",
            "value": 0.019014960599997723,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.objective",
            "value": 0.0003841423999915605,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.gradient",
            "value": 0.0011159358999975667,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.constraints",
            "value": 0.06676118999999972,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.jacobian",
            "value": 0.11635737719999498,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.hessian",
            "value": 0.16865761149999797,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.objective",
            "value": 0.0009743513999978859,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.gradient",
            "value": 0.011886722600002031,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.constraints",
            "value": 0.8345618745000024,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.jacobian",
            "value": 1.4476041053000017,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.hessian",
            "value": 1.929436503699992,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.objective",
            "value": 0.00019801639999741382,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.gradient",
            "value": 0.00037334219999820564,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.constraints",
            "value": 0.004904699899998377,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.jacobian",
            "value": 0.012637931899996601,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.hessian",
            "value": 0.05238334729999679,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.objective",
            "value": 0.0003300007000007099,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.gradient",
            "value": 0.0010266232000049058,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.constraints",
            "value": 0.010406305700007579,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.jacobian",
            "value": 0.1143804580000051,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.hessian",
            "value": 0.5090445498999998,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.objective",
            "value": 0.0009778213000004143,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.gradient",
            "value": 0.011647933699998702,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.constraints",
            "value": 0.0604777403000071,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.jacobian",
            "value": 1.1558202801999982,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.hessian",
            "value": 5.2583734504999935,
            "unit": "sec"
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
          "id": "c3072e7039409bde9a70778d16be97c4472abec7",
          "message": "use 4 tyre submodels instead of just one",
          "timestamp": "2022-05-31T20:59:39+02:00",
          "tree_id": "b37a70907e302022281e9a061eac8b180ccca838",
          "url": "https://github.com/numagic/lumos/commit/c3072e7039409bde9a70778d16be97c4472abec7"
        },
        "date": 1654024484455,
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
            "value": 42.2,
            "unit": "iter"
          },
          {
            "name": "casadi.100.nlp.objective",
            "value": 0.00018884779999552847,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.gradient",
            "value": 0.0004249749999985397,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.constraints",
            "value": 0.01706349969999792,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.jacobian",
            "value": 0.0210772125999938,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.hessian",
            "value": 0.02664161720000493,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.objective",
            "value": 0.00033158610000327826,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.gradient",
            "value": 0.0010189178000018727,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.constraints",
            "value": 0.16725024170000324,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.jacobian",
            "value": 0.20729618560000063,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.hessian",
            "value": 0.2578712144000065,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.objective",
            "value": 0.000894269599996278,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.gradient",
            "value": 0.010041483700001663,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.constraints",
            "value": 1.902762038000003,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.jacobian",
            "value": 2.3721993349999932,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.hessian",
            "value": 2.875458937999997,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.objective",
            "value": 0.00019427769999538213,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.gradient",
            "value": 0.0005220838000013827,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.constraints",
            "value": 0.013362381000001733,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.jacobian",
            "value": 0.021044899599996825,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.hessian",
            "value": 0.05256662460000143,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.objective",
            "value": 0.0003050363000056677,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.gradient",
            "value": 0.0010221278000017264,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.constraints",
            "value": 0.0187707259999911,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.jacobian",
            "value": 0.08873496090000117,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.hessian",
            "value": 0.2784952503999989,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.objective",
            "value": 0.0007802813999887803,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.gradient",
            "value": 0.009739542100010112,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.constraints",
            "value": 0.06695310810000592,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.jacobian",
            "value": 0.7375238236000087,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.hessian",
            "value": 2.626811105800016,
            "unit": "sec"
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
          "id": "08d2fe23c09ffb12e34ab9f77d02becda11414ac",
          "message": "add jit time profiling to metrics",
          "timestamp": "2022-06-01T08:55:43+02:00",
          "tree_id": "f99419f90b788df5003d02ca5bb3aee5c713b40d",
          "url": "https://github.com/numagic/lumos/commit/08d2fe23c09ffb12e34ab9f77d02becda11414ac"
        },
        "date": 1654067502842,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "jax_jit.model_algebra.constraints",
            "value": 2.373652034999992,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.jacobian",
            "value": 11.22342618799999,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.hessian",
            "value": 38.29125423299999,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.objective",
            "value": 0.0002370365000018637,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.gradient",
            "value": 0.00040316400000222074,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.constraints",
            "value": 0.015443260600000031,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.jacobian",
            "value": 0.018802010699999983,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.hessian",
            "value": 0.025030518200000528,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.objective",
            "value": 0.00030158560000188573,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.gradient",
            "value": 0.0009674958000005062,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.constraints",
            "value": 0.1588781871000009,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.jacobian",
            "value": 0.22010643579999964,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.hessian",
            "value": 0.27899894790000135,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.objective",
            "value": 0.0014435387999981232,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.gradient",
            "value": 0.014003974199999903,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.constraints",
            "value": 2.1356567151000037,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.jacobian",
            "value": 2.3204209907000006,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.hessian",
            "value": 2.765895243,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.objective",
            "value": 0.00022269680000022162,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.gradient",
            "value": 0.0004973328000005495,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.constraints",
            "value": 0.013119330399996442,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.jacobian",
            "value": 0.019827163499996914,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.hessian",
            "value": 0.05153157529999817,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.objective",
            "value": 0.00040267400000857376,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.gradient",
            "value": 0.0011881224000035218,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.constraints",
            "value": 0.01866828299999952,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.jacobian",
            "value": 0.08839573980000068,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.hessian",
            "value": 0.3209590929000001,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.objective",
            "value": 0.001069694500006335,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.gradient",
            "value": 0.011797099099999287,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.constraints",
            "value": 0.0725468200000023,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.jacobian",
            "value": 0.8108972920999917,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.hessian",
            "value": 2.632673451200003,
            "unit": "sec"
          },
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
            "value": 42.2,
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
          "id": "8c855e012b5f6d60abe26bafc9da8151d0b46ed3",
          "message": "store feature push benchmark to a separate page\n\n- now benchmarks are stored for all pushes and stored in dev/benchmark-features",
          "timestamp": "2022-06-01T13:40:39+02:00",
          "tree_id": "61499481556b7d1db0c6f2a3be698ba28288ee46",
          "url": "https://github.com/numagic/lumos/commit/8c855e012b5f6d60abe26bafc9da8151d0b46ed3"
        },
        "date": 1654084554111,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "jax_jit.model_algebra.constraints",
            "value": 2.3677301260000263,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.jacobian",
            "value": 11.20133703099998,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.hessian",
            "value": 38.054598037000005,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.objective",
            "value": 0.00023934750000194073,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.gradient",
            "value": 0.0004145355999980893,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.constraints",
            "value": 0.01573415410000507,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.jacobian",
            "value": 0.01933967610000309,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.hessian",
            "value": 0.024213094800001046,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.objective",
            "value": 0.00029447690000097284,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.gradient",
            "value": 0.0009350800999982312,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.constraints",
            "value": 0.15491927760000407,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.jacobian",
            "value": 0.19319800039999677,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.hessian",
            "value": 0.24216090580000013,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.objective",
            "value": 0.0007613719000005403,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.gradient",
            "value": 0.006753147900002432,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.constraints",
            "value": 1.8142328350999946,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.jacobian",
            "value": 2.2878846857999973,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.hessian",
            "value": 2.7165179207999928,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.objective",
            "value": 0.0002139477000014267,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.gradient",
            "value": 0.00045422510000889813,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.constraints",
            "value": 0.012558113199997934,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.jacobian",
            "value": 0.01971460530000968,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.hessian",
            "value": 0.05062346860000844,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.objective",
            "value": 0.00034026629999743817,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.gradient",
            "value": 0.0010392885999976897,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.constraints",
            "value": 0.017671426799995515,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.jacobian",
            "value": 0.08314401070000485,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.hessian",
            "value": 0.2660894756000062,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.objective",
            "value": 0.0007984610999983488,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.gradient",
            "value": 0.007490046800000982,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.constraints",
            "value": 0.06452921339999876,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.jacobian",
            "value": 0.70799095939999,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.hessian",
            "value": 2.5657360616000005,
            "unit": "sec"
          },
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
            "value": 42.2,
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
          "id": "c5585a63cd0d97572a23be51826f3a7c85d8f3b5",
          "message": "update readme to include links to benchmarks",
          "timestamp": "2022-06-01T14:26:26+02:00",
          "tree_id": "fe998be8d5ccc907343a592ea4bc075ff29d9e27",
          "url": "https://github.com/numagic/lumos/commit/c5585a63cd0d97572a23be51826f3a7c85d8f3b5"
        },
        "date": 1654087810591,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "jax_jit.model_algebra.constraints",
            "value": 3.6502239509999868,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.jacobian",
            "value": 16.85752022699998,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.hessian",
            "value": 58.14540983499998,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.objective",
            "value": 0.00031919470000048024,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.gradient",
            "value": 0.0007997267999996893,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.constraints",
            "value": 0.021395515399996158,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.jacobian",
            "value": 0.025671592300000157,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.hessian",
            "value": 0.03313748620000183,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.objective",
            "value": 0.00046186120000015765,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.gradient",
            "value": 0.0016118141999982073,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.constraints",
            "value": 0.279521696300003,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.jacobian",
            "value": 0.3250788031999946,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.hessian",
            "value": 0.3926565439000001,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.objective",
            "value": 0.0010125763000019105,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.gradient",
            "value": 0.014984085899999399,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.constraints",
            "value": 3.186089149900005,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.jacobian",
            "value": 3.8038392793000013,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.hessian",
            "value": 4.4177742613999955,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.objective",
            "value": 0.0003343352000001687,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.gradient",
            "value": 0.0007962461999909465,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.constraints",
            "value": 0.017788088999998307,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.jacobian",
            "value": 0.02785730699999931,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.hessian",
            "value": 0.07445915660000538,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.objective",
            "value": 0.0006316988999969908,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.gradient",
            "value": 0.0017091780999976436,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.constraints",
            "value": 0.02379187730000467,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.jacobian",
            "value": 0.12445117660000733,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.hessian",
            "value": 0.49244641669999967,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.objective",
            "value": 0.0011917645000039557,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.gradient",
            "value": 0.015802732300005572,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.constraints",
            "value": 0.08430514310000489,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.jacobian",
            "value": 1.1482814843000029,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.hessian",
            "value": 5.051400917699993,
            "unit": "sec"
          },
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
            "value": 42.36,
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
          "id": "c599e09097383dbcd4fedd5b93a3fcadaa4d5380",
          "message": "dictionary I/O with automatic outputs collection\n\n- change basic model `forward` I/O from arrays to dictionaries. This is done mainly to reduce the scatter/gather overhead as we pass inputs and outputs between submodels (which doesn't scale well with number of I/O). It also has the added benefits of easier access as we no longer need the 'model' to extract an element from the I/O\r\n- also adds functionality to semi-automatically flatten and assemble submodel outputs into its parent model outputs. The user needs to make one call to combine submodel outputs, and then use them when creating the outputs of the current model. \r\n- rename of states_dot outputs: instead of automatically adding `_dot` to the state name, we now use the same name for states and states_dot, eg, states[\"vx\"] would give you the state vx, and states_dot[\"vx\"] would give you its derivative w.r.t. the mesh",
          "timestamp": "2022-06-03T11:23:14+02:00",
          "tree_id": "b72aedda3077d1853db0bd409c3ccc0ee0c3d55b",
          "url": "https://github.com/numagic/lumos/commit/c599e09097383dbcd4fedd5b93a3fcadaa4d5380"
        },
        "date": 1654249246967,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "jax_jit.model_algebra.constraints",
            "value": 2.3110859180000034,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.jacobian",
            "value": 10.639787882000007,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.hessian",
            "value": 54.90656991499998,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.objective",
            "value": 0.00021641989999920952,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.gradient",
            "value": 0.00043417969999950403,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.constraints",
            "value": 0.015465730299996493,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.jacobian",
            "value": 0.019193049000000427,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.hessian",
            "value": 0.02417161099999703,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.objective",
            "value": 0.0003440707000038401,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.gradient",
            "value": 0.0010467121999965911,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.constraints",
            "value": 0.18609482880000314,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.jacobian",
            "value": 0.2418106722999994,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.hessian",
            "value": 0.28628927880000105,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.objective",
            "value": 0.0009342214000014337,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.gradient",
            "value": 0.010653735599998982,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.constraints",
            "value": 2.3590160682999963,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.jacobian",
            "value": 2.900755436899999,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.hessian",
            "value": 3.3255232489999913,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.objective",
            "value": 0.00024469060000456013,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.gradient",
            "value": 0.00046375100000659584,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.constraints",
            "value": 0.012206067099998563,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.jacobian",
            "value": 0.020286935100000392,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.hessian",
            "value": 0.039783658500005,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.objective",
            "value": 0.0003229004999980134,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.gradient",
            "value": 0.0010240216000056534,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.constraints",
            "value": 0.015618474399991556,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.jacobian",
            "value": 0.10676330689999532,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.hessian",
            "value": 0.26876848020000355,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.objective",
            "value": 0.000956842699997651,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.gradient",
            "value": 0.010303319100000864,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.constraints",
            "value": 0.06916344500000378,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.jacobian",
            "value": 1.0969101845999945,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.hessian",
            "value": 2.7389245374999973,
            "unit": "sec"
          },
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
            "value": 42.4,
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
          "id": "ce8e4cb0ee17da70fa75e2b25dca5924df7231f1",
          "message": "fix logging bugs\n\n- make logging more generic so that it works with all kinds of ocp\r\n- creates more stringent tests for logging\r\n- simplifies logging possibilities: when logging_config is not provided,\r\nnothing is logged, when loggign_config is provided, but\r\nlog_every_nth_iter==0, then only final results and metrics history is\r\nlogged. Otherwise additonally, the result at every nth iteration is\r\nlogged, with the last itertion result also appended.\r\n\r\nNotes:\r\n- the code structure is still not ideal, and can definitely benefit from\r\nsome refactorization. But functionality-wise it should be more robust\r\nnow than before.",
          "timestamp": "2022-06-03T21:04:14+02:00",
          "tree_id": "654974150d610b93067e72e2a2763d67e92be798",
          "url": "https://github.com/numagic/lumos/commit/ce8e4cb0ee17da70fa75e2b25dca5924df7231f1"
        },
        "date": 1654284406771,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "jax_jit.model_algebra.constraints",
            "value": 3.3119651110000063,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.jacobian",
            "value": 14.728994649000015,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.hessian",
            "value": 72.81219679100002,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.objective",
            "value": 0.000322836200001575,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.gradient",
            "value": 0.0006208109999988664,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.constraints",
            "value": 0.019469914699999435,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.jacobian",
            "value": 0.0235931211000036,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.hessian",
            "value": 0.03206586520000201,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.objective",
            "value": 0.0004811828000015339,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.gradient",
            "value": 0.0014586385000029622,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.constraints",
            "value": 0.22673896290000356,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.jacobian",
            "value": 0.2884546871999987,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.hessian",
            "value": 0.3688421495,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.objective",
            "value": 0.0010376915999927405,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.gradient",
            "value": 0.014529672200001186,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.constraints",
            "value": 2.695946786800005,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.jacobian",
            "value": 3.2680711837000103,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.hessian",
            "value": 3.8796638771000063,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.objective",
            "value": 0.00032045010000274486,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.gradient",
            "value": 0.0006538803000012194,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.constraints",
            "value": 0.015779458700001213,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.jacobian",
            "value": 0.02601051430000325,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.hessian",
            "value": 0.05313200919999872,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.objective",
            "value": 0.0007702707000021292,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.gradient",
            "value": 0.0015069512999957625,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.constraints",
            "value": 0.02292440029999625,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.jacobian",
            "value": 0.13227993709999736,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.hessian",
            "value": 0.33254991439999915,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.objective",
            "value": 0.0010232410000071469,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.gradient",
            "value": 0.014909944700002597,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.constraints",
            "value": 0.08295983169998636,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.jacobian",
            "value": 1.2466598279999972,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.hessian",
            "value": 3.215862023500017,
            "unit": "sec"
          },
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
            "value": 42.2,
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
          "id": "f729354613fec84957384323da6d0b69e00ed7cc",
          "message": "code generation and mex compilation\n\n- add method to export state-space model with array I/O to c-code, which can be compiled to mex functions\r\n- add tests to export c-code from a vehicle model and then compile to mex on linux and windows. Tests the\r\nmex executes correctly and gives the expected outputs using octave.",
          "timestamp": "2022-06-05T15:49:36+02:00",
          "tree_id": "aee3a5fb6c369b936a730bb8777925ba6565ad56",
          "url": "https://github.com/numagic/lumos/commit/f729354613fec84957384323da6d0b69e00ed7cc"
        },
        "date": 1654438197929,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "jax_jit.model_algebra.constraints",
            "value": 2.601067927999992,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.jacobian",
            "value": 12.452464711000005,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.hessian",
            "value": 64.21018228,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.objective",
            "value": 0.00025350340000045434,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.gradient",
            "value": 0.000554137400001764,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.constraints",
            "value": 0.018774699200002944,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.jacobian",
            "value": 0.024006198600000063,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.hessian",
            "value": 0.0305540456000017,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.objective",
            "value": 0.0004126654000003782,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.gradient",
            "value": 0.0012525465000010172,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.constraints",
            "value": 0.21659840359999977,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.jacobian",
            "value": 0.2663675081000008,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.hessian",
            "value": 0.31633307769999985,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.objective",
            "value": 0.001117414700001973,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.gradient",
            "value": 0.012116520199998603,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.constraints",
            "value": 2.5603025504000017,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.jacobian",
            "value": 3.128076617000005,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.hessian",
            "value": 3.6475205427999926,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.objective",
            "value": 0.00028843370000686264,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.gradient",
            "value": 0.0005976176999979543,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.constraints",
            "value": 0.013979500699997515,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.jacobian",
            "value": 0.025098184500006938,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.hessian",
            "value": 0.04974155320001046,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.objective",
            "value": 0.0004929663999973854,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.gradient",
            "value": 0.0013388474000066708,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.constraints",
            "value": 0.021931975299992246,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.jacobian",
            "value": 0.13149522030000754,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.hessian",
            "value": 0.3056483154000034,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.objective",
            "value": 0.0010973142000011648,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.gradient",
            "value": 0.010707319400000869,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.constraints",
            "value": 0.08346186640000042,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.jacobian",
            "value": 1.2576336012999945,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.hessian",
            "value": 2.987454169699993,
            "unit": "sec"
          },
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
            "value": 42.4,
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
          "id": "d1e355c5931d2d3dbdddfedb39565014ff5b3f41",
          "message": "removed the requirement to define con_outputs at a model level\n\n- allow con_outputs to be defined dynamically for a simulation via sim_config\r\nentry 'con_output_names'",
          "timestamp": "2022-06-22T17:12:44+02:00",
          "tree_id": "c9967875dfb83f4eb839fc9620f59b55313558a7",
          "url": "https://github.com/numagic/lumos/commit/d1e355c5931d2d3dbdddfedb39565014ff5b3f41"
        },
        "date": 1655911917849,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "jax_jit.model_algebra.constraints",
            "value": 2.362337509000014,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.jacobian",
            "value": 11.062800419000013,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.hessian",
            "value": 57.13782667999999,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.objective",
            "value": 0.00021937370000273403,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.gradient",
            "value": 0.0004637477999978046,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.constraints",
            "value": 0.015899736500000473,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.jacobian",
            "value": 0.021278916700001104,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.hessian",
            "value": 0.026644376600000897,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.objective",
            "value": 0.00036794469999676946,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.gradient",
            "value": 0.0011201545000005808,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.constraints",
            "value": 0.2004168800000002,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.jacobian",
            "value": 0.25687786839999943,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.hessian",
            "value": 0.29920838460000143,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.objective",
            "value": 0.0009946637999973973,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.gradient",
            "value": 0.012534024799998633,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.constraints",
            "value": 2.4559672756,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.jacobian",
            "value": 3.2833147085000007,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.hessian",
            "value": 3.4098549660999993,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.objective",
            "value": 0.00024694349999663243,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.gradient",
            "value": 0.00047146659999270925,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.constraints",
            "value": 0.012851519100001952,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.jacobian",
            "value": 0.022617165199994814,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.hessian",
            "value": 0.04120840429999362,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.objective",
            "value": 0.0004301662999978362,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.gradient",
            "value": 0.0011902073999976893,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.constraints",
            "value": 0.01955454719999352,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.jacobian",
            "value": 0.11764093740000589,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.hessian",
            "value": 0.28689344269999995,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.objective",
            "value": 0.0010636154000053465,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.gradient",
            "value": 0.013964002000000164,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.constraints",
            "value": 0.0769232527999975,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.jacobian",
            "value": 1.13794381539999,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.hessian",
            "value": 2.829533547900007,
            "unit": "sec"
          },
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
            "value": 42.48,
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
          "id": "39dc43b573db7ecd0da465253ca4427a298cc722",
          "message": "Remove submodel names attribute\n\n- now this is made into a class method that retrieves the submodel names\r\ndirectly from get_default_submodel_config, which reduces redundancy\r\nand potential for error",
          "timestamp": "2022-06-22T18:01:31+02:00",
          "tree_id": "276d06d95cc15bbdb4bb6966d0ec8fded776e6dc",
          "url": "https://github.com/numagic/lumos/commit/39dc43b573db7ecd0da465253ca4427a298cc722"
        },
        "date": 1655915062761,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "jax_jit.model_algebra.constraints",
            "value": 3.1426171889999637,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.jacobian",
            "value": 14.022422275999986,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.hessian",
            "value": 68.698598092,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.objective",
            "value": 0.0003548442999999679,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.gradient",
            "value": 0.000681198300003416,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.constraints",
            "value": 0.019528738399998247,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.jacobian",
            "value": 0.025017355400001405,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.hessian",
            "value": 0.03098694820000105,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.objective",
            "value": 0.0005324860000030185,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.gradient",
            "value": 0.0016281385000013414,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.constraints",
            "value": 0.2425959954999996,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.jacobian",
            "value": 0.3040240911000012,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.hessian",
            "value": 0.37237841749999917,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.objective",
            "value": 0.001214860499999304,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.gradient",
            "value": 0.013795629100002316,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.constraints",
            "value": 2.7455754350999997,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.jacobian",
            "value": 3.3329492364999966,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.hessian",
            "value": 4.023275839400003,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.objective",
            "value": 0.00039233470000681335,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.gradient",
            "value": 0.0007074884000076054,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.constraints",
            "value": 0.016417605900005582,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.jacobian",
            "value": 0.028978605800000425,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.hessian",
            "value": 0.05486851550000438,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.objective",
            "value": 0.0005496960999948897,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.gradient",
            "value": 0.0017246892000002845,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.constraints",
            "value": 0.02342639060000238,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.jacobian",
            "value": 0.14292242940000505,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.hessian",
            "value": 0.3707721844999924,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.objective",
            "value": 0.0011270832000036535,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.gradient",
            "value": 0.012833539400003247,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.constraints",
            "value": 0.07553679949999151,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.jacobian",
            "value": 1.355852668900002,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.hessian",
            "value": 3.4652202450000003,
            "unit": "sec"
          },
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
            "value": 42.2,
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
          "id": "9772d4d8a1360386a4b0393d8c6b0e33232f6327",
          "message": "fix typehint to represent dict io",
          "timestamp": "2022-06-23T11:04:09+02:00",
          "tree_id": "50e250a79e6cc6a6ded9d79f34d662996148c5c3",
          "url": "https://github.com/numagic/lumos/commit/9772d4d8a1360386a4b0393d8c6b0e33232f6327"
        },
        "date": 1655976169463,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "jax_jit.model_algebra.constraints",
            "value": 2.3651728179999907,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.jacobian",
            "value": 11.001938454999987,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.hessian",
            "value": 56.33554272400002,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.objective",
            "value": 0.00022590410000020711,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.gradient",
            "value": 0.0004599881999979516,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.constraints",
            "value": 0.015690022600000474,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.jacobian",
            "value": 0.019884888199999295,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.hessian",
            "value": 0.024497061300002086,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.objective",
            "value": 0.0003932370999990553,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.gradient",
            "value": 0.0011087500000002137,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.constraints",
            "value": 0.19939989829999832,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.jacobian",
            "value": 0.252567436999999,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.hessian",
            "value": 0.29801878640000157,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.objective",
            "value": 0.0009948175000033643,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.gradient",
            "value": 0.01300166820000186,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.constraints",
            "value": 2.4819429935000015,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.jacobian",
            "value": 3.0159430574,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.hessian",
            "value": 3.4464197544,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.objective",
            "value": 0.00025222460000122736,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.gradient",
            "value": 0.0004725586000063231,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.constraints",
            "value": 0.012750711400008186,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.jacobian",
            "value": 0.02212443150000354,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.hessian",
            "value": 0.04228046729999733,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.objective",
            "value": 0.0004056165000065448,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.gradient",
            "value": 0.0011403684000015346,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.constraints",
            "value": 0.018575009900007444,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.jacobian",
            "value": 0.11514761879999469,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.hessian",
            "value": 0.2853944198000022,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.objective",
            "value": 0.0010741737999978795,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.gradient",
            "value": 0.012515710299999228,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.constraints",
            "value": 0.07525882359999514,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.jacobian",
            "value": 1.117390431900003,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.hessian",
            "value": 2.814291195999999,
            "unit": "sec"
          },
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
            "value": 42.48,
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
          "id": "eccc155aa7fdff27f4b5dc4d8eae0d45b2e56700",
          "message": "handle decisioni variable scaling manually \n\n- previously the decision variable scaling is done by IPOPT, but now we\r\n  take control of this ourselves to get better convergence and tolerance\r\ncontrol.\r\n- this means the objective, constraints, their derivatives and the\r\n  bounds on the decision variables all need to be scaled by ourselves.",
          "timestamp": "2022-06-23T17:39:08+02:00",
          "tree_id": "aed20c02beef41cea66f3f3341e35b413ab08b4b",
          "url": "https://github.com/numagic/lumos/commit/eccc155aa7fdff27f4b5dc4d8eae0d45b2e56700"
        },
        "date": 1656000207840,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "jax_jit.model_algebra.constraints",
            "value": 3.321379766000007,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.jacobian",
            "value": 15.458194638000009,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.hessian",
            "value": 74.04289600300001,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.objective",
            "value": 0.0003802211999982319,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.gradient",
            "value": 0.0007633123999994495,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.constraints",
            "value": 0.02095451550000007,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.jacobian",
            "value": 0.025737760399999844,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.hessian",
            "value": 0.033114203399998134,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.objective",
            "value": 0.0007093446999988373,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.gradient",
            "value": 0.0020050333000028787,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.constraints",
            "value": 0.24496969440000385,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.jacobian",
            "value": 0.3009115237000003,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.hessian",
            "value": 0.3800878867999984,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.objective",
            "value": 0.002508909099998391,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.gradient",
            "value": 0.021199401500001613,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.constraints",
            "value": 2.985847034400001,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.jacobian",
            "value": 3.6132443316999967,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.hessian",
            "value": 4.3022277708000045,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.objective",
            "value": 0.0004605030999982773,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.gradient",
            "value": 0.0008305355000061354,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.constraints",
            "value": 0.015616052999996554,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.jacobian",
            "value": 0.03138687699999991,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.hessian",
            "value": 0.06255117260000134,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.objective",
            "value": 0.0007020155999953204,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.gradient",
            "value": 0.0025918809000017974,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.constraints",
            "value": 0.026078029400002832,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.jacobian",
            "value": 0.16644904649999717,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.hessian",
            "value": 0.39533528419999586,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.objective",
            "value": 0.002854990800005908,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.gradient",
            "value": 0.020631590499999675,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.constraints",
            "value": 0.0966000546000032,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.jacobian",
            "value": 1.5815885450999985,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.hessian",
            "value": 3.9667293658000062,
            "unit": "sec"
          },
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
            "value": 41.84,
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
          "id": "44966ea310b84d2e9e55cfee43c6ad2b2608c071",
          "message": "make outputs collection more automatic\n\n- create `call_submodel` methods to use instead of getting the submodel\r\n  manually and then calling it. This call also handles input checking,\r\nresult buffering (for automtic colleciton later).\r\n- the submodel returns are now stored in a buffer after it is called.\r\n  The buffer is cleared when the submodel outputs are collected.\r\n- to avoid contamination of results in the buffer:\r\n1) a RuntimeError will be thrown if the corresponding buffer entry\r\n   already exists when a submodel is called (eg, happens when one calls\r\nthe same submodel twice before outputs collection)\r\n2) a KeyError will be thrown if the outputs collection happens before\r\n   all submodels are called",
          "timestamp": "2022-06-24T12:04:25+02:00",
          "tree_id": "bd042a2d261951093718f21df0a02dfd1709c9fd",
          "url": "https://github.com/numagic/lumos/commit/44966ea310b84d2e9e55cfee43c6ad2b2608c071"
        },
        "date": 1656066357856,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "jax_jit.model_algebra.constraints",
            "value": 2.8300904760000094,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.jacobian",
            "value": 12.615446927999983,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.hessian",
            "value": 65.512102169,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.objective",
            "value": 0.0002893044000018108,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.gradient",
            "value": 0.0005659386999980143,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.constraints",
            "value": 0.02006989900000349,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.jacobian",
            "value": 0.027373871399998962,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.hessian",
            "value": 0.032931607099999385,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.objective",
            "value": 0.0006422038999971847,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.gradient",
            "value": 0.001510712700002159,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.constraints",
            "value": 0.217273185199997,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.jacobian",
            "value": 0.2717217541000025,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.hessian",
            "value": 0.3241952819999995,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.objective",
            "value": 0.0026911304000009294,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.gradient",
            "value": 0.01813084269999763,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.constraints",
            "value": 2.515348996599994,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.jacobian",
            "value": 3.184446841700003,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.hessian",
            "value": 3.702830191299995,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.objective",
            "value": 0.00035804390000748754,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.gradient",
            "value": 0.0006014067000023715,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.constraints",
            "value": 0.01505158620000202,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.jacobian",
            "value": 0.028284792299996298,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.hessian",
            "value": 0.05380924410000034,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.objective",
            "value": 0.0006278969000049983,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.gradient",
            "value": 0.001566147300002285,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.constraints",
            "value": 0.02233067580000352,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.jacobian",
            "value": 0.15033372909999798,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.hessian",
            "value": 0.34753668949999794,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.objective",
            "value": 0.0028853177000087273,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.gradient",
            "value": 0.016494998699999996,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.constraints",
            "value": 0.09194255400000202,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.jacobian",
            "value": 1.483547591599995,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.hessian",
            "value": 3.3466890287999944,
            "unit": "sec"
          },
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
            "value": 41.84,
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
          "id": "7c174fada5f8971736101c1fab5003a16e9b8056",
          "message": "version bump to 0.0.2rc4",
          "timestamp": "2022-06-25T07:30:52+02:00",
          "tree_id": "0fa7e6e092ea0cbbd5bd97bb8653511b62baa9a0",
          "url": "https://github.com/numagic/lumos/commit/7c174fada5f8971736101c1fab5003a16e9b8056"
        },
        "date": 1656136124319,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "jax_jit.model_algebra.constraints",
            "value": 2.3297139400000333,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.jacobian",
            "value": 10.742632843000024,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.hessian",
            "value": 55.24768216000001,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.objective",
            "value": 0.00023233349999713938,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.gradient",
            "value": 0.0005164976999992632,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.constraints",
            "value": 0.01798499930000048,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.jacobian",
            "value": 0.021598083300000327,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.hessian",
            "value": 0.024686977199996817,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.objective",
            "value": 0.0006091386000036892,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.gradient",
            "value": 0.0013964899000029618,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.constraints",
            "value": 0.1839599337999971,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.jacobian",
            "value": 0.2273087020000048,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.hessian",
            "value": 0.27022949070000096,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.objective",
            "value": 0.0026831407000031506,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.gradient",
            "value": 0.016980877799994687,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.constraints",
            "value": 2.3912913998000023,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.jacobian",
            "value": 2.8985333287999993,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.hessian",
            "value": 3.309437428000001,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.objective",
            "value": 0.00025298330000396164,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.gradient",
            "value": 0.0005097467000041433,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.constraints",
            "value": 0.01239338200000475,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.jacobian",
            "value": 0.02277160770000819,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.hessian",
            "value": 0.04396486489999916,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.objective",
            "value": 0.0005395769999950062,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.gradient",
            "value": 0.0013673477999986972,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.constraints",
            "value": 0.018627362600000197,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.jacobian",
            "value": 0.12218241110000463,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.hessian",
            "value": 0.28666024280000785,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.objective",
            "value": 0.002360183100006452,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.gradient",
            "value": 0.014901369200003955,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.constraints",
            "value": 0.0760324665999974,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.jacobian",
            "value": 1.210908738699993,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.hessian",
            "value": 2.7813176134999935,
            "unit": "sec"
          },
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
            "value": 41.84,
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
          "id": "02533c54baa5cec2540b1419420762564cef5f52",
          "message": "add interp that works both with jax and casadi\n\nadd interp that works both with jax and casadi\r\n\r\n- the default behaviour for our of range is use end values\r\n- the 'period' functionality is not implemented",
          "timestamp": "2022-06-27T20:28:12+02:00",
          "tree_id": "b82d289f8ca685400836a739e5719882c4b73744",
          "url": "https://github.com/numagic/lumos/commit/02533c54baa5cec2540b1419420762564cef5f52"
        },
        "date": 1656355606272,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "jax_jit.model_algebra.constraints",
            "value": 2.3052678959999753,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.jacobian",
            "value": 10.723944990000007,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.hessian",
            "value": 55.07194621299999,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.objective",
            "value": 0.00025235169999859863,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.gradient",
            "value": 0.0004520130000003064,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.constraints",
            "value": 0.016150055000002793,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.jacobian",
            "value": 0.02181040179999627,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.hessian",
            "value": 0.026757503900000756,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.objective",
            "value": 0.0005035037999959968,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.gradient",
            "value": 0.001276769499997954,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.constraints",
            "value": 0.19135800479999715,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.jacobian",
            "value": 0.23238913120000007,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.hessian",
            "value": 0.27563132399999973,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.objective",
            "value": 0.002234976400001187,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.gradient",
            "value": 0.014833008499999778,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.constraints",
            "value": 2.384453018199997,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.jacobian",
            "value": 2.9130670943999974,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.hessian",
            "value": 3.350976194500004,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.objective",
            "value": 0.0002620418999981666,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.gradient",
            "value": 0.000519803800000318,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.constraints",
            "value": 0.012702371299997139,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.jacobian",
            "value": 0.023319097699993564,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.hessian",
            "value": 0.044414609499995095,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.objective",
            "value": 0.0005597340999997869,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.gradient",
            "value": 0.0013528397999948538,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.constraints",
            "value": 0.019527472200002192,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.jacobian",
            "value": 0.12590902650000543,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.hessian",
            "value": 0.29448117420000697,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.objective",
            "value": 0.00226318679999622,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.gradient",
            "value": 0.014365686700000425,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.constraints",
            "value": 0.0797245625999949,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.jacobian",
            "value": 1.258072176799999,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.hessian",
            "value": 3.0125269068999954,
            "unit": "sec"
          },
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
            "value": 41.84,
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
          "id": "dd2efe83f4f6d04fdaebf534a1e98eb41dd1094a",
          "message": "allow options and includes in cmex export",
          "timestamp": "2022-07-01T09:25:52+02:00",
          "tree_id": "8c3fdf769cc36936b5f2a8d210e6023141629ec8",
          "url": "https://github.com/numagic/lumos/commit/dd2efe83f4f6d04fdaebf534a1e98eb41dd1094a"
        },
        "date": 1656661426604,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "jax_jit.model_algebra.constraints",
            "value": 3.6320565050000084,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.jacobian",
            "value": 12.695656864,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.hessian",
            "value": 54.649390764,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.objective",
            "value": 0.00024890300000208755,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.gradient",
            "value": 0.0004726357000009784,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.constraints",
            "value": 0.014228924299999335,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.jacobian",
            "value": 0.01851770690000194,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.hessian",
            "value": 0.023100783099999946,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.objective",
            "value": 0.0005277766999995492,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.gradient",
            "value": 0.0013253270999996404,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.constraints",
            "value": 0.17198955710000235,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.jacobian",
            "value": 0.20846613520000118,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.hessian",
            "value": 0.2492619087999998,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.objective",
            "value": 0.0024697992999961117,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.gradient",
            "value": 0.01596012900000119,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.constraints",
            "value": 2.190355962800004,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.jacobian",
            "value": 2.6887590846000022,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.hessian",
            "value": 3.140229898199999,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.objective",
            "value": 0.0002693116999978429,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.gradient",
            "value": 0.0005052932000012333,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.constraints",
            "value": 0.01208817709999721,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.jacobian",
            "value": 0.022159941199998912,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.hessian",
            "value": 0.044450053399998524,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.objective",
            "value": 0.0005278325000062978,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.gradient",
            "value": 0.001388696499998332,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.constraints",
            "value": 0.0213431700000001,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.jacobian",
            "value": 0.11653761569999688,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.hessian",
            "value": 0.27982033660000527,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.objective",
            "value": 0.0023445880000053875,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.gradient",
            "value": 0.013991177299999435,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.constraints",
            "value": 0.0729262920999986,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.jacobian",
            "value": 1.0549816119999946,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.hessian",
            "value": 2.560681024900009,
            "unit": "sec"
          },
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
            "value": 42.08,
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
          "id": "92446cd49c282dd3c28d700ec9048a9b3600a651",
          "message": "fix logging issues\n\n- ensure we use the correct decision variables: for some calls we need\r\nunscaled, and for some others we need the scaled ones\r\n- ensure that the cyclic constraints are also logged, so that we don't\r\nmiss the case where the largest infeasibility comes from cyclic\r\nconstraints\r\n\r\nIn addition:\r\n- fix brachistochrone test",
          "timestamp": "2022-08-10T16:04:20+02:00",
          "tree_id": "5d159b67591a065abec46a1ee013c3975e3f11d9",
          "url": "https://github.com/numagic/lumos/commit/92446cd49c282dd3c28d700ec9048a9b3600a651"
        },
        "date": 1660141264481,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "jax_jit.model_algebra.constraints",
            "value": 3.5224032550000004,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.jacobian",
            "value": 11.912307011999985,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.hessian",
            "value": 53.91940118400001,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.objective",
            "value": 0.00019785940000076606,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.gradient",
            "value": 0.00043163859999992835,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.constraints",
            "value": 0.014413904299999558,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.jacobian",
            "value": 0.018239872099999842,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.hessian",
            "value": 0.02284618749999936,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.objective",
            "value": 0.0004561185000000023,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.gradient",
            "value": 0.001173846199998252,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.constraints",
            "value": 0.1521951814000005,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.jacobian",
            "value": 0.18981727830000067,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.hessian",
            "value": 0.23562235900000134,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.objective",
            "value": 0.001901651299999685,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.gradient",
            "value": 0.010818550200002618,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.constraints",
            "value": 1.8066171537000002,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.jacobian",
            "value": 2.3091801910000016,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.hessian",
            "value": 2.7438786023999966,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.objective",
            "value": 0.00021531930000264765,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.gradient",
            "value": 0.00042606869999985977,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.constraints",
            "value": 0.01293675879999796,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.jacobian",
            "value": 0.021447521699997196,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.hessian",
            "value": 0.04101270950000071,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.objective",
            "value": 0.00046882849999292376,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.gradient",
            "value": 0.0012048361999973168,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.constraints",
            "value": 0.018800280200002815,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.jacobian",
            "value": 0.10466975670000238,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.hessian",
            "value": 0.2423636282000075,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.objective",
            "value": 0.0019343238000033125,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.gradient",
            "value": 0.009647978999998941,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.constraints",
            "value": 0.07070121330000348,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.jacobian",
            "value": 0.976359188999993,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.hessian",
            "value": 2.2435477075999986,
            "unit": "sec"
          },
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
            "value": 42.12,
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
          "id": "e2955763be8d8a456f55c0f0d6bc354f51e06813",
          "message": "fix TreeParam bug with casadi and 1d array",
          "timestamp": "2022-08-10T16:39:52+02:00",
          "tree_id": "5fde40e4c0d2b935b828c2d242550283320f5f50",
          "url": "https://github.com/numagic/lumos/commit/e2955763be8d8a456f55c0f0d6bc354f51e06813"
        },
        "date": 1660143483103,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "jax_jit.model_algebra.constraints",
            "value": 3.6451311969999836,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.jacobian",
            "value": 12.475838703000022,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.hessian",
            "value": 58.130282937000004,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.objective",
            "value": 0.00022085270000218315,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.gradient",
            "value": 0.00046200559999931556,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.constraints",
            "value": 0.01531848780000189,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.jacobian",
            "value": 0.019200405400002295,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.hessian",
            "value": 0.024743973300002154,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.objective",
            "value": 0.0005377465999998777,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.gradient",
            "value": 0.0012974659999997584,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.constraints",
            "value": 0.17812648379999985,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.jacobian",
            "value": 0.2190285285000016,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.hessian",
            "value": 0.26647390910000013,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.objective",
            "value": 0.002274039299999231,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.gradient",
            "value": 0.014732589700003018,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.constraints",
            "value": 2.2294885474000012,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.jacobian",
            "value": 2.7390037422000035,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.hessian",
            "value": 3.181978029499999,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.objective",
            "value": 0.00024592299999994795,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.gradient",
            "value": 0.00045346560000325553,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.constraints",
            "value": 0.012974798799996278,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.jacobian",
            "value": 0.023789951100002326,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.hessian",
            "value": 0.04502554089999648,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.objective",
            "value": 0.000562836899996455,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.gradient",
            "value": 0.0013724569000032715,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.constraints",
            "value": 0.019397099200000413,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.jacobian",
            "value": 0.11509800919999406,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.hessian",
            "value": 0.27791988070000573,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.objective",
            "value": 0.0022725063999928354,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.gradient",
            "value": 0.012828398900001047,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.constraints",
            "value": 0.07806670060000442,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.jacobian",
            "value": 1.1276658008000027,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.hessian",
            "value": 2.737556127100004,
            "unit": "sec"
          },
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
            "value": 42.12,
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
          "id": "50295ed989d9018c45c80bef4b5650f861d54ed8",
          "message": "bump version to 0.0.2rc5",
          "timestamp": "2022-08-10T17:15:41+02:00",
          "tree_id": "9267ff19bf7aa1ce5d9699bdbc50fc8441887db0",
          "url": "https://github.com/numagic/lumos/commit/50295ed989d9018c45c80bef4b5650f861d54ed8"
        },
        "date": 1660145568874,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "jax_jit.model_algebra.constraints",
            "value": 3.594488192,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.jacobian",
            "value": 12.093483825999982,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.hessian",
            "value": 55.657342710999984,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.objective",
            "value": 0.0001994803000002321,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.gradient",
            "value": 0.0004268405999994229,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.constraints",
            "value": 0.01506220219999932,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.jacobian",
            "value": 0.01950723870000388,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.hessian",
            "value": 0.02384274500000174,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.objective",
            "value": 0.0005045706999965205,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.gradient",
            "value": 0.0011906716999988021,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.constraints",
            "value": 0.16093016700000362,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.jacobian",
            "value": 0.19704436810000062,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.hessian",
            "value": 0.24431883470000457,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.objective",
            "value": 0.0019068225000012263,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.gradient",
            "value": 0.010658223999996608,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.constraints",
            "value": 1.843164774600001,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.jacobian",
            "value": 2.3302078277999954,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.hessian",
            "value": 2.7629329735,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.objective",
            "value": 0.0002206402999945567,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.gradient",
            "value": 0.0004348606000007749,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.constraints",
            "value": 0.013462897299996257,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.jacobian",
            "value": 0.022861279400001423,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.hessian",
            "value": 0.042770025100003294,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.objective",
            "value": 0.0004666205000035006,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.gradient",
            "value": 0.0011796512999922015,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.constraints",
            "value": 0.020404182499999025,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.jacobian",
            "value": 0.10782741879999094,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.hessian",
            "value": 0.2461011978999977,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.objective",
            "value": 0.002129522600000655,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.gradient",
            "value": 0.01301674589999493,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.constraints",
            "value": 0.0730607594999924,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.jacobian",
            "value": 0.988711098300007,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.hessian",
            "value": 2.273920250399999,
            "unit": "sec"
          },
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
            "value": 42.12,
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
          "id": "74983a474584f9dc10d5ff5bd0666baa73bc704d",
          "message": "more docs and examples for custom objectives\n\n- add more documentation to the methods and objects related to objective\r\n- add a colab notebook for custom objective function",
          "timestamp": "2022-08-23T14:12:55+02:00",
          "tree_id": "1c09fdcb3161c538507c4cf12892cd5311ee47a3",
          "url": "https://github.com/numagic/lumos/commit/74983a474584f9dc10d5ff5bd0666baa73bc704d"
        },
        "date": 1661257939848,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "jax_jit.model_algebra.constraints",
            "value": 3.88030446099998,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.jacobian",
            "value": 13.378447666999989,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.hessian",
            "value": 62.84480689700001,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.objective",
            "value": 0.0002253917000018646,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.gradient",
            "value": 0.0004706933999955254,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.constraints",
            "value": 0.018288132800000766,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.jacobian",
            "value": 0.02269106480000005,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.hessian",
            "value": 0.02787555240000188,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.objective",
            "value": 0.0005233138999983566,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.gradient",
            "value": 0.0013143197999966106,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.constraints",
            "value": 0.1897084940999946,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.jacobian",
            "value": 0.23314874380000106,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.hessian",
            "value": 0.2808838975000015,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.objective",
            "value": 0.0025864410000053795,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.gradient",
            "value": 0.01673297550000825,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.constraints",
            "value": 2.3093210878000034,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.jacobian",
            "value": 2.8224029427999993,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.hessian",
            "value": 3.2892270194000046,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.objective",
            "value": 0.00025634190000118907,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.gradient",
            "value": 0.00048418369999581046,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.constraints",
            "value": 0.013809966299993448,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.jacobian",
            "value": 0.025426965899998776,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.hessian",
            "value": 0.04764806150000141,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.objective",
            "value": 0.0005827237000062269,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.gradient",
            "value": 0.0014159832999894207,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.constraints",
            "value": 0.021776481200004128,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.jacobian",
            "value": 0.12016020190000062,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.hessian",
            "value": 0.29509747480000215,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.objective",
            "value": 0.002863602900004025,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.gradient",
            "value": 0.015431163599998854,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.constraints",
            "value": 0.08129752150000513,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.jacobian",
            "value": 1.1510690178000005,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.hessian",
            "value": 2.8213565321000034,
            "unit": "sec"
          },
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
            "value": 42.12,
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
          "id": "f5d52272bcbbb23d3294f729fb3b48134475d4d9",
          "message": "fix colab notebook path",
          "timestamp": "2022-08-23T14:56:43+02:00",
          "tree_id": "081d5e6c9179c5592a4b7491d9ff0df0d0e76168",
          "url": "https://github.com/numagic/lumos/commit/f5d52272bcbbb23d3294f729fb3b48134475d4d9"
        },
        "date": 1661260499040,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "jax_jit.model_algebra.constraints",
            "value": 3.7905254780000064,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.jacobian",
            "value": 11.666578309000045,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.hessian",
            "value": 59.20882996199998,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.objective",
            "value": 0.00022886329999778355,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.gradient",
            "value": 0.0004792369000028884,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.constraints",
            "value": 0.015831568199996583,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.jacobian",
            "value": 0.020453254899996408,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.hessian",
            "value": 0.02499436030000197,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.objective",
            "value": 0.0005703860999972221,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.gradient",
            "value": 0.0013508945000012319,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.constraints",
            "value": 0.18684954439999615,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.jacobian",
            "value": 0.22758093120000353,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.hessian",
            "value": 0.26613314699999935,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.objective",
            "value": 0.0024236394000013207,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.gradient",
            "value": 0.015776166199998443,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.constraints",
            "value": 2.4243314605999897,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.jacobian",
            "value": 2.882410614999992,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.hessian",
            "value": 3.207437790300003,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.objective",
            "value": 0.0002611922000028244,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.gradient",
            "value": 0.0004778040000019246,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.constraints",
            "value": 0.011722920499994415,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.jacobian",
            "value": 0.021570075200008886,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.hessian",
            "value": 0.04079050029999962,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.objective",
            "value": 0.000579264600003171,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.gradient",
            "value": 0.0013677809000000706,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.constraints",
            "value": 0.018084034000003156,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.jacobian",
            "value": 0.11058321070000829,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.hessian",
            "value": 0.2773776354000006,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.objective",
            "value": 0.002380698800004666,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.gradient",
            "value": 0.014739585999996052,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.constraints",
            "value": 0.07460568720000538,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.jacobian",
            "value": 1.0900704670999972,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.hessian",
            "value": 2.840548424999997,
            "unit": "sec"
          },
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
            "value": 42.12,
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
          "id": "b9016cedbb1335d08ffb2aa921c21580e7a15faf",
          "message": "add functionality to do model algebra solves\n\n- add ModelSolver class to perform algebraic solves on models\r\n- see tests/test_optimal_control/test_model_solver.py for more details\r\n\r\nKnown issue:\r\n- model algebraic solve works for 'casadi' backend only at the moment. Getting other backend\r\nto work is possible but will require some refactoring. However it is unlikely we'll need the 'jax'\r\nbackend for model algebraic solve because this is a single-stage problem, so nothing to\r\nparallelize",
          "timestamp": "2022-09-08T08:38:09+02:00",
          "tree_id": "3f802b9572daa4baac8d89774506d4999f9322db",
          "url": "https://github.com/numagic/lumos/commit/b9016cedbb1335d08ffb2aa921c21580e7a15faf"
        },
        "date": 1662620108332,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "jax_jit.model_algebra.constraints",
            "value": 3.435170155999998,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.jacobian",
            "value": 11.964742682000008,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.hessian",
            "value": 55.02120507499998,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.objective",
            "value": 0.00022612989999970523,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.gradient",
            "value": 0.0004011697999999342,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.constraints",
            "value": 0.015818522500001108,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.jacobian",
            "value": 0.019530890800001543,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.hessian",
            "value": 0.02441278850000117,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.objective",
            "value": 0.00046012010000140435,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.gradient",
            "value": 0.0012069200999974329,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.constraints",
            "value": 0.1616767343000049,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.jacobian",
            "value": 0.20891778839999803,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.hessian",
            "value": 0.2576848503999997,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.objective",
            "value": 0.001961191600003076,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.gradient",
            "value": 0.011592008700000633,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.constraints",
            "value": 1.8351825345000008,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.jacobian",
            "value": 2.323702186600002,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.hessian",
            "value": 2.782401447199999,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.objective",
            "value": 0.0002295201000038105,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.gradient",
            "value": 0.0004503002999967975,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.constraints",
            "value": 0.013140737300000182,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.jacobian",
            "value": 0.02222754240000313,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.hessian",
            "value": 0.04285657399999536,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.objective",
            "value": 0.0005053913999972792,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.gradient",
            "value": 0.0012504433999993125,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.constraints",
            "value": 0.01963855200000353,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.jacobian",
            "value": 0.10729872370000067,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.hessian",
            "value": 0.2422491859999923,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.objective",
            "value": 0.001994425500004127,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.gradient",
            "value": 0.011140090500009591,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.constraints",
            "value": 0.07139875540000276,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.jacobian",
            "value": 0.9946527262000018,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.hessian",
            "value": 2.2894717119999997,
            "unit": "sec"
          },
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
            "value": 42,
            "unit": "iter"
          }
        ]
      }
    ]
  }
}