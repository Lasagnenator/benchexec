# This file is part of BenchExec, a framework for reliable benchmarking:
# https://github.com/sosy-lab/benchexec
#
# SPDX-FileCopyrightText: 2007-2020 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

import benchexec.result as result
import benchexec.tools.template
from benchexec.tools.sv_benchmarks_util import (
    get_witness_options,
    get_non_witness_input_files,
)


class Tool(benchexec.tools.template.BaseTool2):
    """
    Tool info for jcwit
    """

    def executable(self, tool_locator):
        return tool_locator.find_executable("jcwit.py")

    def version(self, executable):
        return self._version_from_tool(executable)

    def name(self):
        return "jcwit"

    def project_url(self):
        return "https://github.com/Chriszai/JCWIT"

    def cmdline(self, executable, options, task, rlimits):
        input_files = get_non_witness_input_files(task)
        witness_options = ["--witness"]
        additional_options = get_witness_options(options, task, witness_options)

        return [executable] + options + additional_options + input_files

    def determine_result(self, run):
        for line in run.output:
            if (
                "Witness result: Unknown" in line
                or "Witness validation: Unknown" in line
            ):
                return result.RESULT_UNKNOWN

            if "Witness result: False" in line or "Witness validation: False" in line:
                return result.RESULT_FALSE_PROP

            if "Witness validation: True" in line:
                return result.RESULT_TRUE_PROP

        return result.RESULT_ERROR
