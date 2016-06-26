from deployment import DeploymentTest
from basic import BasicDeploymentSpec

EXTERNAL = {
    "trusty": "cs:~matsubara/trusty/ci-configurator-3",
}

REPO = "lp:~free.ekanayaka/junk/ci-configurator-test-repo"


class ExternalDeploymentSpec(BasicDeploymentSpec):

    def _pre_setup_10_external(self):
        """Set up the deployment in the class."""
        # XXX ci-configuration is currently broken and needs the paramiko
        #     package.
        self.jenkins_config["tools"] = "python-paramiko"
        # This will trigger removal of plugins set on the principal
        self.jenkins_config["remove-unlisted-plugins"] = "yes"
        self.deployment.add("ci-configurator", EXTERNAL[self.series])
        self.deployment.configure("ci-configurator", {"config-repo":  REPO})
        self.deployment.relate(
            "jenkins:extension", "ci-configurator:jenkins-configurator")


class ExternalDeploymentTest(DeploymentTest):

    def test_00_principal_plugins(self):
        """The plugins set on the jenkins principal are removed."""
        plugins = self.spec.plugins_list()
        self.assertNotIn("groovy", plugins, "Plugin not removed")

    def test_00_requested_plugins(self):
        """The plugins requested by the configurator are there."""
        stat = self.spec.plugin_dir_stat("git")
        self.assertGreater(stat["size"], 0, "Failed to locate plugin")
        stat = self.spec.plugin_dir_stat("git-client")
        self.assertGreater(stat["size"], 0, "Failed to locate plugin")
