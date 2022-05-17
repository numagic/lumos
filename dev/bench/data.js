window.BENCHMARK_DATA = {
  "lastUpdate": 1652795238609,
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
      }
    ]
  }
}