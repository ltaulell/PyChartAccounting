<map version="freeplane 1.7.0">
<!--To view this file, download free mind mapping software Freeplane from http://freeplane.sourceforge.net -->
<node TEXT="PyChartAccounting" FOLDED="false" ID="ID_1847389613" CREATED="1611222274847" MODIFIED="1611304187395" STYLE="oval">
<font SIZE="18"/>
<hook NAME="MapStyle">
    <properties edgeColorConfiguration="#808080ff,#ff0000ff,#0000ffff,#00ff00ff,#ff00ffff,#00ffffff,#7c0000ff,#00007cff,#007c00ff,#7c007cff,#007c7cff,#7c7c00ff" show_note_icons="true" fit_to_viewport="false"/>

<map_styles>
<stylenode LOCALIZED_TEXT="styles.root_node" STYLE="oval" UNIFORM_SHAPE="true" VGAP_QUANTITY="24.0 pt">
<font SIZE="24"/>
<stylenode LOCALIZED_TEXT="styles.predefined" POSITION="right" STYLE="bubble">
<stylenode LOCALIZED_TEXT="default" ICON_SIZE="12.0 pt" COLOR="#000000" STYLE="fork">
<font NAME="SansSerif" SIZE="10" BOLD="false" ITALIC="false"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.details"/>
<stylenode LOCALIZED_TEXT="defaultstyle.attributes">
<font SIZE="9"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.note" COLOR="#000000" BACKGROUND_COLOR="#ffffff" TEXT_ALIGN="LEFT"/>
<stylenode LOCALIZED_TEXT="defaultstyle.floating">
<edge STYLE="hide_edge"/>
<cloud COLOR="#f0f0f0" SHAPE="ROUND_RECT"/>
</stylenode>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.user-defined" POSITION="right" STYLE="bubble">
<stylenode LOCALIZED_TEXT="styles.topic" COLOR="#18898b" STYLE="fork">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.subtopic" COLOR="#cc3300" STYLE="fork">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.subsubtopic" COLOR="#669900">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.important">
<icon BUILTIN="yes"/>
</stylenode>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.AutomaticLayout" POSITION="right" STYLE="bubble">
<stylenode LOCALIZED_TEXT="AutomaticLayout.level.root" COLOR="#000000" STYLE="oval" SHAPE_HORIZONTAL_MARGIN="10.0 pt" SHAPE_VERTICAL_MARGIN="10.0 pt">
<font SIZE="18"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,1" COLOR="#0033ff">
<font SIZE="16"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,2" COLOR="#00b439">
<font SIZE="14"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,3" COLOR="#990000">
<font SIZE="12"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,4" COLOR="#111111">
<font SIZE="10"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,5"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,6"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,7"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,8"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,9"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,10"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,11"/>
</stylenode>
</stylenode>
</map_styles>
</hook>
<hook NAME="AutomaticEdgeColor" COUNTER="6" RULE="ON_BRANCH_CREATION"/>
<node TEXT="besoins" POSITION="right" ID="ID_879044232" CREATED="1611222290374" MODIFIED="1611246389248" HGAP_QUANTITY="13.250000022351742 pt" VSHIFT_QUANTITY="-49.499998524785084 pt">
<edge COLOR="#ff0000"/>
<font SIZE="12" BOLD="true"/>
<node TEXT="analyser le fichier d&apos;accounting &quot;&#xe0; froid&quot;" ID="ID_1458569467" CREATED="1611222295206" MODIFIED="1611222309578"/>
<node TEXT="permettre une visualisation graphique des r&#xe9;sultats" ID="ID_1522155414" CREATED="1611222310694" MODIFIED="1611246807965">
<font BOLD="true"/>
</node>
<node TEXT="ouvrir aux utilisateurs du cluster (intranet)" ID="ID_434819635" CREATED="1611222329271" MODIFIED="1611223609154"/>
<node TEXT="https://rdlab.cs.upc.edu/s-gae/" ID="ID_1762824682" CREATED="1611222433690" MODIFIED="1611222438299"/>
</node>
<node TEXT="fichier d&apos;accounting" POSITION="left" ID="ID_75483259" CREATED="1611222349223" MODIFIED="1611304212096">
<edge COLOR="#0000ff"/>
<richcontent TYPE="NOTE">

<html>
  <head>
    
  </head>
  <body>
    <p>
      d&#233;crit dans :
    </p>
    <p>
      https://github.com/ltaulell/PyChartAccounting/blob/master/SGE_accounting_file_format.rst
    </p>
    <p>
      https://github.com/ltaulell/PyChartAccounting/blob/master/analysis.rst
    </p>
  </body>
</html>

</richcontent>
</node>
<node TEXT="contraintes" POSITION="right" ID="ID_1446962237" CREATED="1611222476841" MODIFIED="1611304187393" HGAP_QUANTITY="37.249999307096026 pt" VSHIFT_QUANTITY="5.99999982118608 pt">
<edge COLOR="#ff00ff"/>
<font SIZE="12" BOLD="true"/>
<node TEXT="python3" ID="ID_1776342741" CREATED="1611222481689" MODIFIED="1611304234185">
<font BOLD="true" ITALIC="true"/>
</node>
<node TEXT="base de donn&#xe9;es ?" ID="ID_1226836252" CREATED="1611222489401" MODIFIED="1611222494252"/>
<node TEXT="client web pour la visualisation" ID="ID_783243255" CREATED="1611222497290" MODIFIED="1611222511581"/>
</node>
<node TEXT="proposition d&apos;architecture" POSITION="left" ID="ID_53254147" CREATED="1611239468368" MODIFIED="1611247087748" HGAP_QUANTITY="22.249999754130847 pt" VSHIFT_QUANTITY="25.4999992400408 pt">
<edge COLOR="#00ffff"/>
<node TEXT="3-tiers" ID="ID_1819904400" CREATED="1611239476432" MODIFIED="1611247083428" HGAP_QUANTITY="28.24999957531692 pt" VSHIFT_QUANTITY="-9.749999709427366 pt">
<node TEXT="si base de donn&#xe9;es, alors postgresql (serveur existant)" ID="ID_1094899213" CREATED="1611239480863" MODIFIED="1611247114705"/>
<node TEXT="backend de remplissage de la bdd (script python3, via cron)" ID="ID_1573433779" CREATED="1611239500016" MODIFIED="1611247076038" HGAP_QUANTITY="27.499999597668662 pt" VSHIFT_QUANTITY="16.499999508261695 pt"/>
<node TEXT="frontend web (id&#xe9;alement python3)" ID="ID_836487610" CREATED="1611239532336" MODIFIED="1611247073021" HGAP_QUANTITY="25.999999642372142 pt" VSHIFT_QUANTITY="17.99999946355821 pt"/>
</node>
</node>
<node TEXT="UseCases" POSITION="right" ID="ID_1837565422" CREATED="1611245989216" MODIFIED="1611304184721" HGAP_QUANTITY="29.749999530613437 pt" VSHIFT_QUANTITY="-23.999999284744284 pt">
<edge COLOR="#7c0000"/>
<richcontent TYPE="NOTE">

<html>
  <head>
    
  </head>
  <body>
    <p>
      Pour faire plus simple, il ne devrait pas y avoir de diff&#233;rence entre Users et Admins
    </p>
  </body>
</html>
</richcontent>
<node TEXT="Users" ID="ID_627672557" CREATED="1611245994423" MODIFIED="1611304093282" HGAP_QUANTITY="19.249999843537815 pt" VSHIFT_QUANTITY="-29.24999912828209 pt">
<node TEXT="sur une p&#xe9;riode donn&#xe9;e (all, year, a period of time)" ID="ID_868386145" CREATED="1611245997639" MODIFIED="1611304109937" HGAP_QUANTITY="20.74999979883433 pt" VSHIFT_QUANTITY="-34.499998971819906 pt">
<node TEXT="myself ou un autre" ID="ID_404668446" CREATED="1611246313997" MODIFIED="1611246326065"/>
<node TEXT="project(s)" ID="ID_45717942" CREATED="1611246072345" MODIFIED="1611304136671"/>
<node TEXT="consommation cpu" ID="ID_218655592" CREATED="1611246334813" MODIFIED="1611246805226">
<font BOLD="true"/>
</node>
<node TEXT="nombre de jobs" ID="ID_758929309" CREATED="1611246369805" MODIFIED="1611304106665" HGAP_QUANTITY="19.999999821186073 pt" VSHIFT_QUANTITY="-8.999999731779106 pt">
<font BOLD="true"/>
</node>
<node TEXT="m&#xe9;tagroup(s)" ID="ID_1021737442" CREATED="1611246548150" MODIFIED="1611304146320">
<node TEXT="de users (ex: IA)" ID="ID_1168987951" CREATED="1611246580514" MODIFIED="1611246600966"/>
<node TEXT="de groupes existants (ex: Bio, Chimistes)" ID="ID_696573978" CREATED="1611246587089" MODIFIED="1611304102471" VSHIFT_QUANTITY="6.74999979883433 pt"/>
</node>
<node TEXT="group(s)" ID="ID_1034782684" CREATED="1611303966283" MODIFIED="1611304122039" VSHIFT_QUANTITY="9.749999709427366 pt"/>
</node>
</node>
<node TEXT="Admins" ID="ID_77612205" CREATED="1611246304080" MODIFIED="1611304088548">
<node TEXT="sur une p&#xe9;riode donn&#xe9;e" ID="ID_708775162" CREATED="1611246395214" MODIFIED="1611304088545" HGAP_QUANTITY="13.250000022351742 pt" VSHIFT_QUANTITY="40.49999879300598 pt">
<node TEXT="tout ce que peut demander un User" ID="ID_1784434225" CREATED="1611246418383" MODIFIED="1611246629254"/>
<node TEXT="top10 queue(s), host(s)" ID="ID_1299621014" CREATED="1611246427759" MODIFIED="1611246461907"/>
<node TEXT="inverted top10 queue(s), host(s)" ID="ID_642240746" CREATED="1611246443856" MODIFIED="1611246456579"/>
<node TEXT="cluster(s) (groupe de hosts)" ID="ID_318891278" CREATED="1611246838522" MODIFIED="1611304167535"/>
</node>
</node>
</node>
</node>
</map>
