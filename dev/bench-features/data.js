window.BENCHMARK_DATA = {
  "lastUpdate": 1654087903980,
  "repoUrl": "https://github.com/numagic/lumos",
  "entries": {
    "Benchmark": [
      {
        "commit": {
          "author": {
            "email": "yunlong@numagic.io",
            "name": "yunlongxu",
            "username": "yunlongxu-numagic"
          },
          "committer": {
            "email": "yunlong@numagic.io",
            "name": "yunlongxu",
            "username": "yunlongxu-numagic"
          },
          "distinct": true,
          "id": "3ee2f1c03341248e39420ad515b2725f749af998",
          "message": "restore the real tests",
          "timestamp": "2022-06-01T11:07:45Z",
          "tree_id": "61499481556b7d1db0c6f2a3be698ba28288ee46",
          "url": "https://github.com/numagic/lumos/commit/3ee2f1c03341248e39420ad515b2725f749af998"
        },
        "date": 1654082682076,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "jax_jit.model_algebra.constraints",
            "value": 2.4894456450000177,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.jacobian",
            "value": 11.936657295999993,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.hessian",
            "value": 40.703066232,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.objective",
            "value": 0.00021497400000214384,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.gradient",
            "value": 0.00048702900000137107,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.constraints",
            "value": 0.015698632900000575,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.jacobian",
            "value": 0.019292499900001304,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.hessian",
            "value": 0.024602018900000643,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.objective",
            "value": 0.00040917759999956613,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.gradient",
            "value": 0.0011483513000001722,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.constraints",
            "value": 0.18093946749999928,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.jacobian",
            "value": 0.22432313179999994,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.hessian",
            "value": 0.26905689980000036,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.objective",
            "value": 0.0009210765999966952,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.gradient",
            "value": 0.00962078320000046,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.constraints",
            "value": 2.234841311500003,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.jacobian",
            "value": 2.7613242183000013,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.hessian",
            "value": 3.208765259699999,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.objective",
            "value": 0.0002530946999968364,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.gradient",
            "value": 0.000521089600005098,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.constraints",
            "value": 0.012835765799997035,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.jacobian",
            "value": 0.021229249900000014,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.hessian",
            "value": 0.057649838899999396,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.objective",
            "value": 0.0004210478000004514,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.gradient",
            "value": 0.0011360408000086863,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.constraints",
            "value": 0.018387297399999624,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.jacobian",
            "value": 0.09589720959999112,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.hessian",
            "value": 0.3346853370999952,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.objective",
            "value": 0.0009453874000087126,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.gradient",
            "value": 0.010735887500004537,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.constraints",
            "value": 0.07055884829999286,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.jacobian",
            "value": 0.8399150601000087,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.hessian",
            "value": 3.4898331642000016,
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
            "email": "yunlong@numagic.io",
            "name": "yunlongxu",
            "username": "yunlongxu-numagic"
          },
          "committer": {
            "email": "yunlong@numagic.io",
            "name": "yunlongxu",
            "username": "yunlongxu-numagic"
          },
          "distinct": true,
          "id": "b1117f1cddba8c6e5618b9227401387b75795ed1",
          "message": "move to 4 tires per vehicle\n\n- and also makes perantoni tire model compatible with new IO",
          "timestamp": "2022-06-01T11:22:40Z",
          "tree_id": "21f53cdad52fb86e83cd39075a02b3ac81261935",
          "url": "https://github.com/numagic/lumos/commit/b1117f1cddba8c6e5618b9227401387b75795ed1"
        },
        "date": 1654083617309,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "jax_jit.model_algebra.constraints",
            "value": 2.3007504930000096,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.jacobian",
            "value": 10.81743012100003,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.hessian",
            "value": 55.36095221099998,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.objective",
            "value": 0.0002120324999964396,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.gradient",
            "value": 0.0004441753000037352,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.constraints",
            "value": 0.016011970800002474,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.jacobian",
            "value": 0.020503224399999454,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.hessian",
            "value": 0.0265022958999964,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.objective",
            "value": 0.00036031449999995857,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.gradient",
            "value": 0.0010814535999998042,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.constraints",
            "value": 0.18388356610000187,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.jacobian",
            "value": 0.23579382579999902,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.hessian",
            "value": 0.2817926424999996,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.objective",
            "value": 0.0008985809000023437,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.gradient",
            "value": 0.01109987470000533,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.constraints",
            "value": 2.2522408695999956,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.jacobian",
            "value": 2.7703451853000045,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.hessian",
            "value": 3.200916295800005,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.objective",
            "value": 0.00022809269999015668,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.gradient",
            "value": 0.0004567654000084076,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.constraints",
            "value": 0.012424506599995767,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.jacobian",
            "value": 0.021019738000006782,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.hessian",
            "value": 0.04117264580000892,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.objective",
            "value": 0.00043491569999787316,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.gradient",
            "value": 0.001211945799991554,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.constraints",
            "value": 0.018680103200006216,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.jacobian",
            "value": 0.10871343219999971,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.hessian",
            "value": 0.2625306153999986,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.objective",
            "value": 0.0009319416000039382,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.gradient",
            "value": 0.009274924800001827,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.constraints",
            "value": 0.07071448540000347,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.jacobian",
            "value": 1.0633561146000035,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.hessian",
            "value": 2.5673092209999937,
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
            "email": "yunlong@numagic.io",
            "name": "yunlongxu",
            "username": "yunlongxu-numagic"
          },
          "committer": {
            "email": "yunlong@numagic.io",
            "name": "yunlongxu",
            "username": "yunlongxu-numagic"
          },
          "distinct": true,
          "id": "f672daa6fbfb27cd2895e930ea5b2db3aac975e9",
          "message": "experiment: add 500 outputs to vehicle model\n\n- this is just to plot the benchmark results to see if output size\naffects performance without changing constraint output size\n- this should be reverted",
          "timestamp": "2022-06-01T11:22:04Z",
          "tree_id": "ca92df4030282846d63b395ec51b82267e27ffaf",
          "url": "https://github.com/numagic/lumos/commit/f672daa6fbfb27cd2895e930ea5b2db3aac975e9"
        },
        "date": 1654083698714,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "jax_jit.model_algebra.constraints",
            "value": 2.5457730670000274,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.jacobian",
            "value": 12.838792098999988,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.hessian",
            "value": 44.79389462400002,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.objective",
            "value": 0.00021987279999962083,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.gradient",
            "value": 0.0009508419000042068,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.constraints",
            "value": 0.02169779129999938,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.jacobian",
            "value": 0.023430342900002187,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.hessian",
            "value": 0.029763692100004846,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.objective",
            "value": 0.00041215580000084626,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.gradient",
            "value": 0.001190976799995269,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.constraints",
            "value": 0.2126672728000017,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.jacobian",
            "value": 0.25728133570000294,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.hessian",
            "value": 0.2935536669000044,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.objective",
            "value": 0.00101104430000305,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.gradient",
            "value": 0.0163315501999989,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.constraints",
            "value": 2.5640373511000005,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.jacobian",
            "value": 3.0924272443000005,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.hessian",
            "value": 3.6140951908999908,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.objective",
            "value": 0.00027890369999568066,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.gradient",
            "value": 0.0006041278999987298,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.constraints",
            "value": 0.014107904800005145,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.jacobian",
            "value": 0.02394576370001005,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.hessian",
            "value": 0.06490815020000582,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.objective",
            "value": 0.0004058555999904456,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.gradient",
            "value": 0.0011346656999990045,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.constraints",
            "value": 0.01961454140000569,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.jacobian",
            "value": 0.10992323089999445,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.hessian",
            "value": 0.41295154360000197,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.objective",
            "value": 0.0010854150000000119,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.gradient",
            "value": 0.013687108700003137,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.constraints",
            "value": 0.07891690839999228,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.jacobian",
            "value": 0.9537163130000067,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.hessian",
            "value": 4.419725397599995,
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
            "email": "yunlong@numagic.io",
            "name": "yunlongxu",
            "username": "yunlongxu-numagic"
          },
          "committer": {
            "email": "yunlong@numagic.io",
            "name": "yunlongxu",
            "username": "yunlongxu-numagic"
          },
          "distinct": true,
          "id": "1ffd47edeb4aa789823540ef8fdd5bcfa41fa0a9",
          "message": "fix bug of duplicate leafnode collection",
          "timestamp": "2022-06-01T11:21:41Z",
          "tree_id": "819be259bf8f6dbb7bebc044625af4b69f4ad5ac",
          "url": "https://github.com/numagic/lumos/commit/1ffd47edeb4aa789823540ef8fdd5bcfa41fa0a9"
        },
        "date": 1654083758923,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "jax_jit.model_algebra.constraints",
            "value": 2.722946247999971,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.jacobian",
            "value": 21.441454532000023,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.hessian",
            "value": 56.45735293900003,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.objective",
            "value": 0.00020407100000170432,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.gradient",
            "value": 0.0004111720000025798,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.constraints",
            "value": 0.0170880330999978,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.jacobian",
            "value": 0.02126844340000389,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.hessian",
            "value": 0.025856085800000983,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.objective",
            "value": 0.00029069139999933214,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.gradient",
            "value": 0.0010400250000031975,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.constraints",
            "value": 0.1863116424999987,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.jacobian",
            "value": 0.22918490789999738,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.hessian",
            "value": 0.27236956510000143,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.objective",
            "value": 0.0008963342000015473,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.gradient",
            "value": 0.011150542699999733,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.constraints",
            "value": 2.2784712190999925,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.jacobian",
            "value": 2.7827926166999988,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.hessian",
            "value": 3.2307651677999956,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.objective",
            "value": 0.0002490599999987353,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.gradient",
            "value": 0.0005246697999950811,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.constraints",
            "value": 0.01250506699999505,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.jacobian",
            "value": 0.027395843399995103,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.hessian",
            "value": 0.06737220379999372,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.objective",
            "value": 0.00043608000000858735,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.gradient",
            "value": 0.0012115499000060481,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.constraints",
            "value": 0.01816742879999538,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.jacobian",
            "value": 0.13535107100000232,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.hessian",
            "value": 0.4708419900000081,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.objective",
            "value": 0.0009570743999915976,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.gradient",
            "value": 0.009553324000000885,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.constraints",
            "value": 0.07192962369999804,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.jacobian",
            "value": 1.152291952600001,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.hessian",
            "value": 5.152688602600006,
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
            "value": 42.52,
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
        "date": 1654084551714,
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
            "email": "92360845+yunlongxu-numagic@users.noreply.github.com",
            "name": "Yunlong Xu",
            "username": "yunlongxu-numagic"
          },
          "distinct": true,
          "id": "6ee0d302e7cbaf6cc800987fc55d8ee25cdfe01d",
          "message": "update readme to inlaced links to benchmarks",
          "timestamp": "2022-06-01T13:40:54+02:00",
          "tree_id": "fe998be8d5ccc907343a592ea4bc075ff29d9e27",
          "url": "https://github.com/numagic/lumos/commit/6ee0d302e7cbaf6cc800987fc55d8ee25cdfe01d"
        },
        "date": 1654085001987,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "jax_jit.model_algebra.constraints",
            "value": 3.616042878000002,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.jacobian",
            "value": 16.420876835,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.hessian",
            "value": 57.59035260499999,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.objective",
            "value": 0.00031807170000206495,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.gradient",
            "value": 0.0006699337000043215,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.constraints",
            "value": 0.022407992699999112,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.jacobian",
            "value": 0.026147203200002876,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.hessian",
            "value": 0.03294381039999621,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.objective",
            "value": 0.0006688536000012846,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.gradient",
            "value": 0.0015104183000005378,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.constraints",
            "value": 0.2366193321999958,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.jacobian",
            "value": 0.29557805410000243,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.hessian",
            "value": 0.3588513894000016,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.objective",
            "value": 0.0011534261999997853,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.gradient",
            "value": 0.014706329699998832,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.constraints",
            "value": 2.7148816956000017,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.jacobian",
            "value": 3.3177294579999965,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.hessian",
            "value": 3.9255800751000036,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.objective",
            "value": 0.00034149179999758416,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.gradient",
            "value": 0.0006589733999931013,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.constraints",
            "value": 0.01778290099999822,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.jacobian",
            "value": 0.02899217829999543,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.hessian",
            "value": 0.07476720240000531,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.objective",
            "value": 0.0005422541000029924,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.gradient",
            "value": 0.00171421279999322,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.constraints",
            "value": 0.024840566299997136,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.jacobian",
            "value": 0.12088174660000277,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.hessian",
            "value": 0.47625336840000043,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.objective",
            "value": 0.001073675899999671,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.gradient",
            "value": 0.015406954699994913,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.constraints",
            "value": 0.08854052670000101,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.jacobian",
            "value": 1.092624740000008,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.hessian",
            "value": 4.708789399,
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
            "email": "yunlong@numagic.io",
            "name": "yunlongxu",
            "username": "yunlongxu-numagic"
          },
          "committer": {
            "email": "yunlong@numagic.io",
            "name": "yunlongxu",
            "username": "yunlongxu-numagic"
          },
          "distinct": true,
          "id": "84f63d63d1369f7ae86785baa8bf782e7153e8f4",
          "message": "working laptime simulations and vehicle tests\n\n- modified the necessary models to use the new IO\n\nproblems:\n- jax compilation time much longer than before (160sec for hessian\ninstead of 27sec) where does that come from?\n- execution time is roughtly the same for both backends\n- and also makes perantoni tire model compatible with new IO",
          "timestamp": "2022-06-01T12:28:06Z",
          "tree_id": "4b48431c96228047078b13119fa1b0a6bd5bccca",
          "url": "https://github.com/numagic/lumos/commit/84f63d63d1369f7ae86785baa8bf782e7153e8f4"
        },
        "date": 1654087572117,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "jax_jit.model_algebra.constraints",
            "value": 2.317260516999994,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.jacobian",
            "value": 10.892646643000006,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.hessian",
            "value": 56.01857349000002,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.objective",
            "value": 0.0002191030000005867,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.gradient",
            "value": 0.00046121629999902326,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.constraints",
            "value": 0.017268806699996732,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.jacobian",
            "value": 0.021481404400003613,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.hessian",
            "value": 0.02713005189999649,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.objective",
            "value": 0.00038911529999836604,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.gradient",
            "value": 0.001174256100000548,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.constraints",
            "value": 0.19183979910000062,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.jacobian",
            "value": 0.24500792270000032,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.hessian",
            "value": 0.29248384250000187,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.objective",
            "value": 0.0009414428000013686,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.gradient",
            "value": 0.010884986999997182,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.constraints",
            "value": 2.2971905953999965,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.jacobian",
            "value": 2.8212120394999998,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.hessian",
            "value": 3.279819321299999,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.objective",
            "value": 0.00024299320000409352,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.gradient",
            "value": 0.0004681462000007741,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.constraints",
            "value": 0.01319737520000217,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.jacobian",
            "value": 0.023253308599998947,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.hessian",
            "value": 0.04191574630000332,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.objective",
            "value": 0.00046200620000718117,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.gradient",
            "value": 0.0012458766000008835,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.constraints",
            "value": 0.019411368800001584,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.jacobian",
            "value": 0.11113926189999575,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.hessian",
            "value": 0.26988090849999935,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.objective",
            "value": 0.0010059985999987474,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.gradient",
            "value": 0.012227625700006683,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.constraints",
            "value": 0.07238463579999461,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.jacobian",
            "value": 1.0781346176999933,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.hessian",
            "value": 2.5885614257000045,
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
            "email": "yunlong@numagic.io",
            "name": "yunlongxu",
            "username": "yunlongxu-numagic"
          },
          "committer": {
            "email": "yunlong@numagic.io",
            "name": "yunlongxu",
            "username": "yunlongxu-numagic"
          },
          "distinct": true,
          "id": "41c4bbbb3c1bcedf7583b96c72f33f680ce44d5a",
          "message": "experiment: add 500 outputs to vehicle model\n\n- this is just to plot the benchmark results to see if output size\naffects performance without changing constraint output size\n- this should be reverted",
          "timestamp": "2022-06-01T12:29:04Z",
          "tree_id": "f80108267e0abd2bb4e4184e45d16b42d109e64b",
          "url": "https://github.com/numagic/lumos/commit/41c4bbbb3c1bcedf7583b96c72f33f680ce44d5a"
        },
        "date": 1654087615119,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "jax_jit.model_algebra.constraints",
            "value": 2.5866890080000076,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.jacobian",
            "value": 12.703074115999982,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.hessian",
            "value": 41.58494683500001,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.objective",
            "value": 0.00022423159999789276,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.gradient",
            "value": 0.0004739133999976275,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.constraints",
            "value": 0.01744587700000011,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.jacobian",
            "value": 0.022206701699997212,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.hessian",
            "value": 0.028066104300000914,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.objective",
            "value": 0.0003955935000021782,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.gradient",
            "value": 0.0011114297999995416,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.constraints",
            "value": 0.1905821990999982,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.jacobian",
            "value": 0.23324411120000263,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.hessian",
            "value": 0.2777003746000048,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.objective",
            "value": 0.0009151075000033871,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.gradient",
            "value": 0.011126301400003058,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.constraints",
            "value": 2.318430729200003,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.jacobian",
            "value": 2.8499529096000003,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.hessian",
            "value": 3.301615285599996,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.objective",
            "value": 0.0002659024000081445,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.gradient",
            "value": 0.0005527649000100609,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.constraints",
            "value": 0.01313108709999824,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.jacobian",
            "value": 0.02200013610000724,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.hessian",
            "value": 0.05880593440000439,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.objective",
            "value": 0.00039197329999751673,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.gradient",
            "value": 0.0011222297000017534,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.constraints",
            "value": 0.01948148830000491,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.jacobian",
            "value": 0.09864347200000338,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.hessian",
            "value": 0.36671558890000144,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.objective",
            "value": 0.0010194497000043158,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.gradient",
            "value": 0.01131811770000013,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.constraints",
            "value": 0.07151654800001098,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.jacobian",
            "value": 0.8492610591000016,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.hessian",
            "value": 3.890778311400004,
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
        "date": 1654087808315,
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
            "email": "yunlong@numagic.io",
            "name": "yunlongxu",
            "username": "yunlongxu-numagic"
          },
          "committer": {
            "email": "yunlong@numagic.io",
            "name": "yunlongxu",
            "username": "yunlongxu-numagic"
          },
          "distinct": true,
          "id": "03df194e88bd0b6d60d319aea2268e544085a532",
          "message": "fix bug of duplicate leafnode collection",
          "timestamp": "2022-06-01T12:29:37Z",
          "tree_id": "6528612c037f753221f7320f938be93bb978e4fd",
          "url": "https://github.com/numagic/lumos/commit/03df194e88bd0b6d60d319aea2268e544085a532"
        },
        "date": 1654087902971,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "jax_jit.model_algebra.constraints",
            "value": 2.7790755750000073,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.jacobian",
            "value": 22.48218755000002,
            "unit": "sec"
          },
          {
            "name": "jax_jit.model_algebra.hessian",
            "value": 59.01233429199999,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.objective",
            "value": 0.00020696259999795075,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.gradient",
            "value": 0.000395295100003068,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.constraints",
            "value": 0.016189537899998642,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.jacobian",
            "value": 0.021117411099999116,
            "unit": "sec"
          },
          {
            "name": "casadi.100.nlp.hessian",
            "value": 0.026357698399999664,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.objective",
            "value": 0.00028723230000196056,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.gradient",
            "value": 0.0010130381999999827,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.constraints",
            "value": 0.19441153910000253,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.jacobian",
            "value": 0.23377057980000018,
            "unit": "sec"
          },
          {
            "name": "casadi.1000.nlp.hessian",
            "value": 0.27567112339999655,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.objective",
            "value": 0.0009249221000004581,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.gradient",
            "value": 0.012122997900002019,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.constraints",
            "value": 2.433283873800002,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.jacobian",
            "value": 2.9384628249,
            "unit": "sec"
          },
          {
            "name": "casadi.10000.nlp.hessian",
            "value": 3.4244440758999986,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.objective",
            "value": 0.00024843310000051134,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.gradient",
            "value": 0.0005502869999986614,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.constraints",
            "value": 0.013321699000005082,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.jacobian",
            "value": 0.028403140199998234,
            "unit": "sec"
          },
          {
            "name": "jax.100.nlp.hessian",
            "value": 0.07151234680000015,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.objective",
            "value": 0.0004489757999976973,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.gradient",
            "value": 0.0012443861000065227,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.constraints",
            "value": 0.01932027919999655,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.jacobian",
            "value": 0.14268632690000232,
            "unit": "sec"
          },
          {
            "name": "jax.1000.nlp.hessian",
            "value": 0.532676117699998,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.objective",
            "value": 0.000991752599998108,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.gradient",
            "value": 0.012158145500006868,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.constraints",
            "value": 0.07394181460000482,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.jacobian",
            "value": 1.2195106581999995,
            "unit": "sec"
          },
          {
            "name": "jax.10000.nlp.hessian",
            "value": 5.9369871633999995,
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
            "value": 42.52,
            "unit": "iter"
          }
        ]
      }
    ]
  }
}