using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Xml;

namespace CustomWireshark
{
    public class XmlEx
    {
        XmlDocument _doc = new XmlDocument();
        string _savePath = string.Empty;

        public void Create(string fullPath, string rootName)
        {
            XmlDeclaration decl = _doc.CreateXmlDeclaration("1.0", "utf-8", null);

            _doc.InsertBefore(decl, _doc.DocumentElement);
            XmlNode root = _doc.CreateElement(rootName);
            _doc.AppendChild(root);

            _doc.Save(fullPath);

            _savePath = fullPath;
        }
        public void Open(string fullPath)
        {
            _doc.Load(fullPath);

            _savePath = fullPath;
        }

        public void Save()
        {
            _doc.Save(_savePath);
        }

        public void SaveAs(string fullPath)
        {
            _doc.Save(fullPath);
        }

        public int GetNumberOfChilds(string nodeFullPath)
        {
            XmlNode nodes = _doc.SelectSingleNode(nodeFullPath);
            return nodes.ChildNodes.Count;
        }

        public void CreateNode(string parentNodeName, string childNodeName, string childNodeValue, string attributeName = "",
            string attributeValue = "", string matchedParentAttributName = "", string matchedParentAttirbuteValue = "")
        {
            XmlNode parentNode = null;
            if (matchedParentAttributName == "")
                parentNode = _doc.SelectSingleNode(parentNodeName);
            else
            {
                bool isBreak = false;
                int pos = parentNodeName.LastIndexOf('/');
                string grandParentPath = parentNodeName.Substring(0, pos);
                XmlNode grandParentNode = _doc.SelectSingleNode(grandParentPath);
                foreach (XmlNode parent in grandParentNode.ChildNodes)
                {
                    foreach (XmlAttribute attribute in parent.Attributes)
                    {
                        if (attribute.Name == matchedParentAttributName)
                        {
                            if (attribute.Value == matchedParentAttirbuteValue)
                            {
                                parentNode = parent;
                                isBreak = true;
                                break;
                            }
                        }
                    }

                    if (isBreak == true) break;
                }
            }

            XmlElement childNode = _doc.CreateElement(childNodeName);
            childNode.InnerText = childNodeValue;
            if (attributeName != "" && attributeValue != "")
                childNode.SetAttribute(attributeName, attributeValue);
            parentNode.AppendChild(childNode);
        }

        public void GetNodeAttribute(string parentNodeName, string childNodeName, out string value,
            string matchedParentAttributName = "", string matchedParentAttirbuteValue = "", string matchedChildAttributeName = "")
        {
            bool isBreak = false;
            XmlNode parentNode = null;
            if (matchedParentAttributName == "")
                parentNode = _doc.SelectSingleNode(parentNodeName);
            else
            {
                int pos = parentNodeName.LastIndexOf('/');
                string grandParentPath = parentNodeName.Substring(0, pos);
                XmlNode grandParentNode = _doc.SelectSingleNode(grandParentPath);
                foreach (XmlNode parent in grandParentNode.ChildNodes)
                {
                    foreach (XmlAttribute attribute in parent.Attributes)
                    {
                        if (attribute.Name == matchedParentAttributName)
                        {
                            if (attribute.Value == matchedParentAttirbuteValue)
                            {
                                parentNode = parent;
                                isBreak = true;
                                break;
                            }
                        }
                    }

                    if (isBreak == true) break;
                }
            }

            isBreak = false;
            XmlNodeList childNodes = parentNode.ChildNodes;
            value = "";

            foreach (XmlNode node in childNodes)
            {
                if (node.Name == childNodeName)
                {
                    foreach (XmlAttribute attribute in node.Attributes)
                    {
                        if (attribute.Name == matchedChildAttributeName)
                        {
                            value = attribute.Value;
                            isBreak = true;
                            break;
                        }
                    }
                }
                if (isBreak == true) break;
            }
        }

        public List<string> GetNodeAttributes(string parentNodeName, string childNodeName,
            string matchedParentAttributName = "", string matchedParentAttirbuteValue = "", string matchedChildAttributeName = "")
        {
            List<string> attributes = new List<string>();
            bool isBreak = false;
            XmlNode parentNode = null;
            if (matchedParentAttributName == "")
                parentNode = _doc.SelectSingleNode(parentNodeName);
            else
            {
                int pos = parentNodeName.LastIndexOf('/');
                string grandParentPath = parentNodeName.Substring(0, pos);
                XmlNode grandParentNode = _doc.SelectSingleNode(grandParentPath);
                foreach (XmlNode parent in grandParentNode.ChildNodes)
                {
                    foreach (XmlAttribute attribute in parent.Attributes)
                    {
                        if (attribute.Name == matchedParentAttributName)
                        {
                            if (attribute.Value == matchedParentAttirbuteValue)
                            {
                                parentNode = parent;
                                isBreak = true;
                                break;
                            }
                        }
                    }

                    if (isBreak == true) break;
                }
            }

            isBreak = false;
            XmlNodeList childNodes = parentNode.ChildNodes;

            foreach (XmlNode node in childNodes)
            {
                if (node.Name == childNodeName)
                {
                    foreach (XmlAttribute attribute in node.Attributes)
                    {
                        if (attribute.Name == matchedChildAttributeName)
                        {
                            attributes.Add(attribute.Value);
                        }
                    }
                }
            }

            return attributes;
        }

        public void GetNodeValue(string parentNodeName, string childNodeName, out string value,
            string matchedParentAttributName = "", string matchedParentAttirbuteValue = "")
        {
            XmlNode parentNode = null;
            if (matchedParentAttributName == "")
                parentNode = _doc.SelectSingleNode(parentNodeName);
            else
            {
                bool isBreak = false;
                int pos = parentNodeName.LastIndexOf('/');
                string grandParentPath = parentNodeName.Substring(0, pos);
                XmlNode grandParentNode = _doc.SelectSingleNode(grandParentPath);
                foreach (XmlNode parent in grandParentNode.ChildNodes)
                {
                    foreach (XmlAttribute attribute in parent.Attributes)
                    {
                        if (attribute.Name == matchedParentAttributName)
                        {
                            if (attribute.Value == matchedParentAttirbuteValue)
                            {
                                parentNode = parent;
                                isBreak = true;
                                break;
                            }
                        }
                    }

                    if (isBreak == true) break;
                }
            }

            XmlNodeList childNodes = parentNode.ChildNodes;
            value = "";

            foreach (XmlNode node in childNodes)
            {
                if (node.Name == childNodeName)
                {
                    value = node.InnerText;
                    break;
                }
            }
        }

        public void RemoveNode(string parentNodeName, string childNodeName, string matchedParentAttributName = "", string matchedParentAttirbuteValue = ""
            , string matchedChildAttributName = "", string matchedChildAttirbuteValue = "")
        {
            bool isBreak = false;
            XmlNode parentNode = null;
            if (matchedParentAttributName == "")
                parentNode = _doc.SelectSingleNode(parentNodeName);
            else
            {
                int pos = parentNodeName.LastIndexOf('/');
                string grandParentPath = parentNodeName.Substring(0, pos);
                XmlNode grandParentNode = _doc.SelectSingleNode(grandParentPath);
                foreach (XmlNode parent in grandParentNode.ChildNodes)
                {
                    foreach (XmlAttribute attribute in parent.Attributes)
                    {
                        if (attribute.Name == matchedParentAttributName)
                        {
                            if (attribute.Value == matchedParentAttirbuteValue)
                            {
                                parentNode = parent;
                                isBreak = true;
                                break;
                            }
                        }
                    }

                    if (isBreak == true) break;
                }
            }

            isBreak = false;
            XmlNodeList childNodes = parentNode.ChildNodes;

            foreach (XmlNode child in childNodes)
            {
                if (child.Name == childNodeName)
                {
                    if (matchedChildAttributName == "")
                    {
                        parentNode.RemoveChild(child);
                        isBreak = true;
                        break;
                    }
                    else
                    {
                        foreach (XmlAttribute attribute in child.Attributes)
                        {
                            if (attribute.Name == matchedChildAttributName)
                            {
                                if (attribute.Value == matchedChildAttirbuteValue)
                                {
                                    parentNode.RemoveChild(child);
                                    isBreak = true;
                                    break;
                                }
                            }
                        }
                    }
                }

                if (isBreak == true) break;
            }
        }

        public void EditNodeValue(string parentNodeName, string childNodeName, string childNodeValue, string matchedParentAttributName = "", string matchedParentAttirbuteValue = ""
            , string matchedChildAttributName = "", string matchedChildAttirbuteValue = "")
        {
            bool isBreak = false;
            XmlNode parentNode = null;
            if (matchedParentAttributName == "")
                parentNode = _doc.SelectSingleNode(parentNodeName);
            else
            {
                int pos = parentNodeName.LastIndexOf('/');
                string grandParentPath = parentNodeName.Substring(0, pos);
                XmlNode grandParentNode = _doc.SelectSingleNode(grandParentPath);
                foreach (XmlNode parent in grandParentNode.ChildNodes)
                {
                    foreach (XmlAttribute attribute in parent.Attributes)
                    {
                        if (attribute.Name == matchedParentAttributName)
                        {
                            if (attribute.Value == matchedParentAttirbuteValue)
                            {
                                parentNode = parent;
                                isBreak = true;
                                break;
                            }
                        }
                    }

                    if (isBreak == true) break;
                }
            }

            isBreak = false;
            XmlNodeList childNodes = parentNode.ChildNodes;

            foreach (XmlNode child in childNodes)
            {
                if (child.Name == childNodeName)
                {
                    if (matchedChildAttributName == "")
                    {
                        child.InnerText = childNodeValue;
                        isBreak = true;
                        break;
                    }
                    else
                    {
                        foreach (XmlAttribute attribute in child.Attributes)
                        {
                            if (attribute.Name == matchedChildAttributName)
                            {
                                if (attribute.Value == matchedChildAttirbuteValue)
                                {
                                    child.InnerText = childNodeValue;
                                    isBreak = true;
                                    break;
                                }
                            }
                        }
                    }
                }

                if (isBreak == true) break;
            }
        }
        public void EditNodeValueByName(string parameterFullPath, string parameterValue)
        {
            XmlNode nodeAllowRules = _doc.SelectSingleNode(parameterFullPath); //rules/allow/rule/name
            nodeAllowRules.InnerText = parameterValue;
        }
    }
}
